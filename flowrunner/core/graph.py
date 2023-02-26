import click
from dataclasses import dataclass, field

from typing import Any


@dataclass
class Node:
    """A class that contains the node object
    Attributes:
        name: A str value of the name of the function __name__
        function_reference: The actual function or callable
        next: None by default, list value of what is next node
    """
    name: str
    function_reference: callable
    next: list = field(default_factory=lambda: list())

    def __repr__(self):
        return self.name

# class to handle the seperation of functions
@dataclass
class GraphOptions:
    """A class to manage the options we
    supply to the Graph class
    Attributes:
        - module:
        - functions:
        - middle_nodes:
        - start:
        - end:
    """
    # list of functions/module
    module: Any
    functions: dict = field(default_factory=lambda: dict())
    middle_nodes: list = field(default_factory=lambda: list())
    start: list = field(default_factory=lambda: list())
    end: list = field(default_factory=lambda: list())

    def __post_init__(self):
        # if module get the list of functions
        if not isinstance(self.module, list):
            self.functions = self.module.__dict__
        # if list of functions directly iterate over them
        elif isinstance(self.module, list):
            self.functions = {func.__name__: func for func in  self.module}
        # iterate over list of functions
        # find the start
        # find the end
        for name_func, func in self.functions.items():
            if callable(func):
                # the ones with step, start and end in them
                if hasattr(func, "is_step") and not hasattr(func, "is_start") and not hasattr(func, "is_end") :
                    self.middle_nodes.append(Node(name_func, func))
                elif hasattr(func, "is_step") and hasattr(func, "is_start"):
                    self.start.append(Node(name_func, func))
                elif hasattr(func, "is_step") and hasattr(func, "is_end"):
                    self.end.append(Node(name_func, func))

    def __repr__(self):
        return f"Start={self.start}\nMiddle Nodes={self.middle_nodes}\nEnd={self.end}"






@dataclass
class Graph:
    """FlowRunner is a class to run all steps in a flow
    Attributes:
        graph: A list of graph
        index: A dictionary containing the index and
    """
    graph_options: GraphOptions

    def __post_init__(self):
        """Method to arrange the start, middle and end nodes
        We assign the following attributes
            self.start
            self.middle_nodes
            self.end
            self.nodes
            self.node_map: A dict with names of functions as keys and Node object as value.
            This makes it easy to pick up the node from the name

        """
        self.start = self.graph_options.start
        self.middle_nodes = self.graph_options.middle_nodes
        self.end = self.graph_options.end
        self.nodes = self.start + self.middle_nodes + self.end
        self.node_map = {node.name: node for node in self.nodes}


    def validate_graph(self):
        """Method to validate any graph. Things to check for
        - There should be atleast 1 start
        - There should be atleast 1 end
        - There should be atleast 1 middle
        - All start nodes have a next value
        - All middle nodes have a next value
        - Any step that is not a next for any function
        - An end that has a next value
        """
        pass


    def _arrange_graph(self):
        """Method to traverse graph and arrange into
        self.levels and self.edges
        """
        # create temp_node = start
        temp_level = self.start
        print(temp_level)
        # while loop for when temp_level is not empty
        while not temp_level:
            next_level = []
            # iterate through temp node
            for node in temp_level:
                next = node.function_reference.next
            # find the next of each
            # assign that next as node.next of current node
            # put each of those a new list
            # now that new list is temp_level

    def generate_html(self):
        """A method to generate the html page"""
        pass

    def run_flow(self):
        """A method to run the graph"""
        pass






def run_flow():
    pass