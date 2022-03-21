from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ecs_patterns as ecs_patterns,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_secretsmanager as secretsmanager,
    pipelines
)
import aws_cdk as cdk
from constructs import Construct
from .bus_patrol_challenge_stage import ApplicationStage


class PipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        pipeline = pipelines.CodePipeline(self, "Pipeline",
                                          synth=pipelines.ShellStep("Synth",
                                                                    # Use a connection created using the AWS console to authenticate to GitHub
                                                                    # Other sources are available.
                                                                    input=pipelines.CodePipelineSource.connection(
                                                                        "dhruv9115/bus_patrol_challenge", "main",
                                                                        connection_arn="arn:aws:codestar-connections:us-east-1:705110607627:connection/1977dfaa-7450-41e6-88f1-e950c37343be"
                                                                    ),
                                                                    commands=["npm install -g aws-cdk",
                                                                              "python -m pip install -r requirements.txt", "cdk synth"
                                                                              ]
                                                                    )
                                          )

        pipeline.add_stage(ApplicationStage(self, "Prod",
                                            env=cdk.Environment(
                                                account="705110607627",
                                                region="us-east-1"
                                            )
                                            ))

