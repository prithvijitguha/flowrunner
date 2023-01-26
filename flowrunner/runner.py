import flow_example
import click
from dataclasses import dataclass, field

from typing import Any


@dataclass
class FlowRunner:
    """FlowRunner is a class to run all steps in a flow
    Attributes:
        graph: A list of graph
        index: A dictionary containing the index and

    """

    module: Any
    # [
    #   {'first_function': ['next_func1', 'next_func2'],}
    #   {'next_func1': ['next_func3'], 'next_func2' : ['next_func4', 'next_func5']}
    #   {'next_func1': ['next_func3'], 'next_func2' : ['next_func4', 'next_func5']}
    # ]
    graph: list = field(default_factory=lambda: list())
    index: dict = field(default_factory=lambda: dict())
    nodes: list = field(default_factory=lambda: list())
    start: list = field(default_factory=lambda: list())
    end: list = field(default_factory=lambda: list())
    node_func_map: dict = field(default_factory=lambda: dict())

    def __post_init__(self):
        """This function is to setup the nodes
        and edges for the graph"""
        # get the values for nodes list
        # get the start and end nodes list
        for name, value in self.module.__dict__.items():
            if callable(value):
                if hasattr(value, "is_step"):
                    self.nodes.append(name)
                if hasattr(value, "is_start"):
                    self.start.append(name)
                if hasattr(value, "is_end"):
                    self.end.append(name)
            # store the name of the function against the actual reference of the function in a dict
            self.node_func_map[name] = value

    def _traverse_graph(self):
        """Function to traverse the graph"""
        # add all the edges to the graph
        for value in self.module.__dict__.values():
            if callable(value) and hasattr(value, "is_step"):
                # check the next value and add it as edge
                click.secho(value.name, fg="green")
                click.secho(value.__doc__, fg="bright_red")
                click.secho(f"==>Next Callable: {value.next}\n", fg="blue")

    def _create_graph(self):
        # {
        #   'first_func': ['next_func1', 'next_func2']
        # }
        # start will always be the start
        # self.graph.append()
        # [0: [], ,-1:[]]
        # find the next of start
        # assign the index
        # assign the node
        # assign the edges
        # append to after list
        # end will always be the end
        pass


flow = FlowRunner(flow_example)
# flow.validate()
flow._create_graph()
flow._traverse_graph()
