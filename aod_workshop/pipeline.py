from aws_cdk import (
    core,
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_iam as iam,
    aws_ecr as ecr,
    aws_s3 as s3,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_ec2 as ec2,
)
from aws_cdk.aws_s3 import Bucket
import boto3
REGION = boto3.session.Session().region_name
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']
class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, repo_name: str=None,
                  branch_name: str="master",**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        ecr_repo = ecr.Repository(
            self,
            "EcrRepo",
            repository_name=f"{ACCOUNT_ID}ecr-repo",
            removal_policy=core.RemovalPolicy.DESTROY,
            )
        code_bucket = s3.Bucket(
            self,
            "PipelineBucket",
            bucket_name=f"{construct_id}-pipeline-bucket",
            )
            
        model_bucket = s3.Bucket(
            self,
            "ModelBucket",
            bucket_name=f"{construct_id}-model-bucket",
            )
            
        data_bucket = s3.Bucket(
            self,
            "DataBucket",
            bucket_name=f"{construct_id}-data-bucket",
            )
        code_repo = codecommit.Repository.from_repository_name(self, "CDKRepo",
                  repo_name)
        # build docker image and push to ECR
        cdk_build = codebuild.PipelineProject(self, "CdkBuild",
                        build_spec=codebuild.BuildSpec.from_source_filename(
                            filename='staging/model-code/buildspec.yml'
                            ),
                        environment=codebuild.BuildEnvironment(
                            build_image=codebuild.LinuxBuildImage.STANDARD_3_0,
                            privileged=True),
                        environment_variables={
                            "AWS_DEFAULT_REGION": codebuild.BuildEnvironmentVariable(
                                value=REGION),
                            "IMAGE_REPO_NAME": codebuild.BuildEnvironmentVariable(
                                value=ecr_repo.repository_name),
                            "IMAGE_TAG": codebuild.BuildEnvironmentVariable(
                                value="latest"),
                            "AWS_ACCOUNT_ID": codebuild.BuildEnvironmentVariable(
                                value=ACCOUNT_ID),
                        }
                    )
        ecr_repo.grant_pull_push(cdk_build)
        training_job = tasks.SageMakerCreateTrainingJob(
            self,
            "TrainingJob",
            algorithm_specification=tasks.AlgorithmSpecification(
                training_image=tasks.DockerImage.from_ecr_repository(
                    repository=ecr_repo,
                    tag="latest",
                    )
                ),
            input_data_config=[
                tasks.Channel(
                    channel_name="training",
                    data_source=tasks.DataSource(
                        s3_data_source=tasks.S3DataSource(
                            s3_location=tasks.S3Location.from_bucket(bucket=data_bucket, key_prefix="input")
                            )
                        )
                    ),
                ],
            output_data_config=tasks.OutputDataConfig(
                s3_output_location=tasks.S3Location.from_bucket(bucket=model_bucket, key_prefix="output"),
                ),
            training_job_name=f"{construct_id}-training-job-v5",
            integration_pattern=sfn.IntegrationPattern.RUN_JOB,
            )
        model_create_job = tasks.SageMakerCreateModel(
            self,
            "CreateModel",
            model_name=f"{construct_id}-model",
            primary_container=tasks.ContainerDefinition(
                image=tasks.DockerImage.from_ecr_repository(
                    repository=ecr_repo,
                    tag="latest"
                    ),
                model_s3_location=tasks.S3Location.from_bucket(
                    bucket=model_bucket,
                    key_prefix=f"output/{construct_id}-training-job-v5/output/model.tar.gz"
                    ),
                ),
            )
        model_bucket.grant_read_write(model_create_job)
        endpoint_config_job = tasks.SageMakerCreateEndpointConfig(
            self,
            "CreateEndpointConfig",
            endpoint_config_name=f"{construct_id}-endpoint-config",
            production_variants =[
                tasks.ProductionVariant(
                    instance_type=ec2.InstanceType("m4.xlarge"),
                    model_name=f"{construct_id}-model",
                    initial_instance_count=1,
                    initial_variant_weight=1,
                    variant_name="prod",
                    )]
            )
        endpoint_job = tasks.SageMakerCreateEndpoint(
            self,
            "CreateEndpoint",
            endpoint_config_name=f"{construct_id}-endpoint-config",
            endpoint_name=f"{construct_id}-endpoint",
            )
        definition = sfn.Chain.start(training_job) \
            .next(model_create_job) \
            .next(endpoint_config_job) \
            .next(endpoint_job)
        state_machine = sfn.StateMachine(
            self,
            "StateMachine",
            definition=definition,
            timeout=core.Duration.minutes(10),
            )
        state_machine.add_to_role_policy(iam.PolicyStatement(
            actions=["sagemaker:*"],
            effect=iam.Effect.ALLOW,
            resources=[f"arn:aws:sagemaker:*:{ACCOUNT_ID}:*"]
            ))
        state_machine.add_to_role_policy(iam.PolicyStatement(
            actions=["events:PutTargets", "events:PutRule", "events:DescribeRule"],
            effect=iam.Effect.ALLOW,
            resources=[f"arn:aws:events:*:{ACCOUNT_ID}:rule/*"]
            ))
        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact("BuildOutput")
        deploy_output = codepipeline.Artifact("DeployOutput")
        code_pipeline = codepipeline.Pipeline(
            self,
            "Pipeline",
            artifact_bucket=code_bucket,
            pipeline_name=f"{construct_id}-PipelineStack",
            stages=[
                codepipeline.StageProps(stage_name="Source",
                    actions=[
                        codepipeline_actions.CodeCommitSourceAction(
                            action_name="CDK_Source",
                            repository=code_repo,
                            branch=branch_name,
                            output=source_output)]),
                codepipeline.StageProps(stage_name="Build",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name="CDK_Build",
                            project=cdk_build,
                            input=source_output,
                            outputs=[build_output])]),
                codepipeline.StageProps(stage_name="Deploy",
                    actions=[
                        codepipeline_actions.StepFunctionInvokeAction(
                            state_machine=state_machine,
                            execution_name_prefix="CDKDeploy",
                            action_name="CDK_Deploy",
                            )
                        ]
                    )
                    ]
                    )
        core.CfnOutput(
            self,
            "ECR URI",
            description="ECR Repository URI",
            value=ecr_repo.repository_uri,
            )
        
        core.CfnOutput(
            self,
            "S3 Bucket - Data",
            description="S3 bucket containing training data",
            value=data_bucket.bucket_name,
            )
        
        core.CfnOutput(
            self,
            "S3 Bucket - Code",
            description="S3 bucket containing code",
            value=code_bucket.bucket_name,
            )
            
        core.CfnOutput(
            self,
            "S3 Bucket - Model artifacts",
            description="S3 bucket containing model artifacts",
            value=model_bucket.bucket_name,
            )
            
        core.CfnOutput(
            self,
            "Step function ARN",
            description="ARN of Step Function State Machine",
            value=state_machine.state_machine_arn,
            )
        # create step function tasks
        # events for sync training job
        # cloudformation outputs 
