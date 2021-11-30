from aws_cdk import (
    core,
    aws_sagemaker as sagemaker,
    aws_iam as iam,
    aws_codecommit as codecommit,
    )


class SagemakerStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.sagemaker_execution_role = iam.Role(
            self,
            "CDKSageMakerExecutionRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            role_name=f"{construct_id}-CDKSageMakerExecutionRole",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSageMakerFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "CloudWatchFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonEC2ContainerRegistryFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AWSCodeCommitFullAccess"),
                    ]
        )

        self.code_repository=codecommit.CfnRepository(
            self,
            "CDKRepository",
            repository_name=f"{construct_id}-CDKDefaultRepository",
            )
            
        self.sagemaker_notebook = sagemaker.CfnNotebookInstance(
            self,
            "CDKSageMakerNotebook",
            instance_type="ml.t3.medium",
            role_arn=self.sagemaker_execution_role.role_arn,
            default_code_repository=self.code_repository.attr_clone_url_http,
            volume_size_in_gb=10,
            notebook_instance_name=f"{construct_id}-CDKNotebookInstance",
            )
