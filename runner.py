import flow_example
from flowrunner.core.graph import GraphOptions, Graph


graph_options = GraphOptions(flow_example)
print(graph_options)
graph = Graph(
    nodes=graph_options.nodes,
    start=graph_options.start,
    end=graph_options.end,
    node_func_map=graph_options.node_func_map
    )

graph._create_graph()


