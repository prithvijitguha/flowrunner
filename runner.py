import flow_example

from class_flow_example import FlowExample
from flowrunner.core.graph import GraphOptions, Graph



# graph_options = GraphOptions(FlowExample)
# #print(graph_options)

# graph = Graph(graph_options=graph_options)

# graph._arrange_graph()

# graph.run_flow()
#graph._traverse_graph()

FlowExample().validate_flow()
FlowExample().validate_flow_with_error()
#FlowExample().run_flow()



