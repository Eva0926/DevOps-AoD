#!/usr/bin/env python3
import os
import time
# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from aod_workshop.pipeline import PipelineStack
from aod_workshop.sagemaker_stack import SagemakerStack
from aod_workshop.step_function_stack import StepfunctionStack

app = core.App()
time = int(time.time())
id = f'{time}'
sagemaker_stack = SagemakerStack(app, "sagemaker-stack")
pipeline_stack = PipelineStack(
    app, construct_id = "pipeline-stack", id = id,
    repo_name=sagemaker_stack.code_repository.repository_name)

app.synth()
