from aws_cdk import (
    Stage
)
from .bus_patrol_challenge_stack import BusPatrolChallengeStack


class ApplicationStage(Stage):
    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)
        BusPatrolChallengeStack(self, "App")
