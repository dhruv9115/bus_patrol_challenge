import aws_cdk as core
import aws_cdk.assertions as assertions

from bus_patrol_challenge.bus_patrol_challenge_stack import BusPatrolChallengeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in bus_patrol_challenge/bus_patrol_challenge_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BusPatrolChallengeStack(app, "bus-patrol-challenge")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
