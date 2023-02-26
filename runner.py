import flow_example

import class_flow_example
from flowrunner.core.graph import GraphOptions, Graph


graph_options = GraphOptions(class_flow_example)
#print(graph_options)

graph = Graph(graph_options=graph_options)

graph._arrange_graph()

graph.run_flow()
#graph._traverse_graph()


