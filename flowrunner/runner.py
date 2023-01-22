import flow_example
import click
from dataclasses import dataclass, field
from networkx import DiGraph
from typing import Any

@dataclass
class FlowRunner:
    """FlowRunner is a class to run all steps in a flow"""
    module: Any
    graph: DiGraph = field(default_factory=lambda: DiGraph())
    def __post_init__(self):
        """This function is to setup the nodes
        and edges for the graph"""
        # nodes are a dict of key: value pairs
        # eg. {'example_function': <function example_function at 0x000002DA548CE9D0>,
        self.nodes = {name: value for name, value in self.module.__dict__.items() if callable(value) and hasattr(value, 'is_step')}
        # edges are combination of function names we get it from the 'next' value in parameters
        # eg. [('example_function', 'example_second_function'), ('example_second_function', 'example_third_function')]
        self.edges = [(func_name, actual_func.next) for  func_name, actual_func in  self.nodes.items()]

    def validate(self):
        """Function to validate a FlowRun"""
        # iterate over functions
        # we only need to check for the second value in tuple
        # since the first value we get from the actual function itself
        for edge in self.edges:
            next = edge[1]
            # check if they are all 'steps'
            # check if their next is in the dir()
            if next not in dir(self.module):
                click.secho(f"Node: {next} not in graph", fg='magenta')


    def _traverse_graph(self):
        """Function to traverse the graph"""
        # add all the edges to the graph
        # self.graph.add_edges_from(self.edges)
        # print(self.graph)
        for value in self.module.__dict__.values():
            if callable(value) and hasattr(value, 'is_step'):
                # check the next value and add it as edge
                click.secho(value.name, fg='green')
                click.secho(value.__doc__, fg='bright_red')
                click.secho(f"Next Callable: {value.next}", fg='blue')
                click.echo("\n")


flow = FlowRunner(flow_example)
flow.validate()
flow._traverse_graph()





