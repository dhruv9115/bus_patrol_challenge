import os
from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ecs_patterns as ecs_patterns,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_secretsmanager as secretsmanager
)
from constructs import Construct

from aws_cdk.aws_ecr_assets import DockerImageAsset

from aws_cdk.aws_iam import ManagedPolicy


def docker_build_asset(self, image_id):
    src_root_dir = os.path.join(os.path.dirname(__file__), "..")
    asset = DockerImageAsset(self, image_id, directory=src_root_dir, exclude=['*/cdk.out'])

    return asset


class BusPatrolChallengeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Using default VPC
        vpc = ec2.Vpc.from_lookup(self, "TheVPC", is_default=True)

        # Create Cluster

        cluster = ecs.Cluster(self, id="Cluster", vpc=vpc)

        # Create ALB

        src_root_dir = os.path.join(os.path.dirname(__file__), "..")

        task_role = iam.Role(self, 'taskrole', assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com'))
        task_role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name(managed_policy_name="AmazonEC2ContainerRegistryPowerUser"))
        task_role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name(managed_policy_name="AmazonS3FullAccess"))

        execution_role = iam.Role(self, 'taskexecutionrole', assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com'))
        execution_role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name(managed_policy_name="AmazonEC2ContainerRegistryPowerUser"))
        execution_role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name(managed_policy_name="AmazonS3FullAccess"))

        service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "CreateS3Service", cluster=cluster, cpu=256,
                                                           desired_count=1,
                                                           task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                                               image=ecs.ContainerImage.from_asset(
                                                                   directory=src_root_dir, exclude=['*/cdk.out']),
                                                           execution_role=execution_role,
                                                           task_role=task_role), memory_limit_mib=512,
                                                           public_load_balancer=True, assign_public_ip=True)


        ssm.StringParameter(self, "Parameter",
                            allowed_pattern=".*",
                            description="Role ARN for BOTO3",
                            parameter_name="RoleARN",
                            string_value=execution_role.role_arn,
                            tier=ssm.ParameterTier.ADVANCED
                            )

