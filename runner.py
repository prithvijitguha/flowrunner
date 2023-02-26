import flow_example
import another_flow_example
from flowrunner.core.graph import GraphOptions, Graph, run_flow


graph_options = GraphOptions(another_flow_example)
#print(graph_options)

graph = Graph(graph_options=graph_options)

graph._arrange_graph()


#graph._traverse_graph()


