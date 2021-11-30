
# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    core,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_iam as iam
    )


class StepfunctionStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, training_img: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.training_job = tasks.SageMakerCreateTrainingJob(
            self,
            "CDKTrainingJob",
            algorithm_specification=tasks.AlgorithmSpecification(
                training_image=training_img,
                ),
            input_data_config=[
                tasks.Channel(
                    channel_name="train",
                    data_source=tasks.DataSource(s3_data_source=f"{bucket_name}/input")
                    ),
                ],
            output_data_config=tasks.OutputDataConfig(s3_output_location=f"{bucket_name}/output"),
            training_job_name=f"{construct_id}TrainingJob",
            )
            
        self.model_create_job = tasks.SageMakerCreateModel(
            self,
            "CDKCreateModel",
            model_name=f"{construct_id}SLModel",
            primary_container=training_img,
            )
        self.endpoint_config_job = tasks.SageMakerCreateEndpointConfig(
            self,
            "CDKCreateEndpointConfig",
            endpoint_config_name=f"{construct_id}SLEndpointConfig",
            production_variants =[
                tasks.ProductionVariant(
                    instance_type="ml.m4.xlarge",
                    model_name=f"{construct_id}SLModel",
                    initial_instance_count=1,
                    initial_variant_weight=1
                    )]
            )
        
        self.endpoint_job = tasks.SageMakerCreateEndpoint(
            self,
            "CDKCreateEndpoint",
            endpoint_config_name=f"{construct_id}SLEndpointConfig",
            endpoint_name=f"{construct_id}SLEndpoint",
            )
            
        training_job_start = sfn.Task(
            self, 
            "StartTrainingJob",
            task=self.training_job,
            result_path='$',
            )
        create_model = sfn.Task(
            self,
            "CreateModel",
            task=self.model_create_job,
            result_path='$'
            )
        create_endpoint_config = sfn.Task(
            self,
            "CreateEndpointConfig",
            task=self.endpoint_config_job,
            result_path='$'
            )
        create_endpoint = sfn.Task(
            self,
            "CreateEndpoint",
            task=self.endpoint_job,
            result_path='$'
            )
            
        definition = sfn.Chain.start(training_job_start) \
            .next(create_model) \
            .next(create_endpoint_config) \
            .next(create_endpoint) \
            .next(sfn.Succeed(self, "Success"))
            
        sfn.StateMachine(
            self,
            "StateMachine",
            definition=definition,
            timepout=core.Duration.minutes(10),
            )