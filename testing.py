from class_flow_example import FlowExample
from flowrunner.core.flow import FlowRunner

FlowExample().validate_flow() # we validate the flow

#FlowExample().validate_flow_with_error() # we validate the flow and throw an exception if its not valid

flow_runner = FlowRunner(FlowExample)

print("\n\nRunning with FlowRunner Class")
flow_runner.run_flow()

print("\n\nRunning with run_flow() method")
FlowExample().run_flow()


