from class_flow_example import FlowExample
from flowrunner.core.graph import FlowRunner

FlowExample().validate_flow() # we validate the flow

FlowExample().validate_flow_with_error() # we validate the flow and throw an exception if its not valid

# FlowExample().run_flow()

flow_runner = FlowRunner(FlowExample)

flow_runner.run_flow()


