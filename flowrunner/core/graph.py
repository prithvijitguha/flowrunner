import click
from dataclasses import dataclass, field

from typing import Any


# class to handle the seperation of functions
@dataclass
class GraphOptions:
    # list of functions/module
    module: Any
    functions: dict = field(default_factory=lambda: dict())
    nodes: list = field(default_factory=lambda: list())
    start: list = field(default_factory=lambda: list())
    end: list = field(default_factory=lambda: list())
    node_func_map: dict = field(default_factory=lambda: dict())

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
        # node_func_map
        for name_func, func in self.functions.items():
            if callable(func):
                # the ones with step, start and end in them
                if hasattr(func, "is_step"):
                    self.nodes.append(name_func)
                if hasattr(func, "is_start"):
                    self.start.append(name_func)
                if hasattr(func, "is_end"):
                    self.end.append(name_func)
                self.node_func_map[name_func] = func

    def __repr__(self):
        repr_string = "Nodes=[" + ", ".join([i for i in self.nodes]) + "]"
        return repr_string

@dataclass
class Node:
    """A class that contains the node object"""
    name: str
    function_reference: callable


@dataclass
class Graph:
    """FlowRunner is a class to run all steps in a flow
    Attributes:
        graph: A list of graph
        index: A dictionary containing the index and

    """
    nodes: list
    start: list
    end: list
    node_func_map: dict
    graph: list = field(default_factory=lambda: list())
    index: dict = field(default_factory=lambda: dict())

    # graph = # [
    #   1st Level
    #   {'first_function': ['next_func1', 'next_func2'],}
    #   2nd Level
    #   {'next_func1': ['next_func3'], 'next_func2' : ['next_func4', 'next_func5']}
    #   3rd Level
    #   {'next_func1': ['next_func3'], 'next_func2' : ['next_func4', 'next_func5']}
    # ]
    def _traverse_graph(self):
        """Function to traverse the graph"""
        # add all the edges to the graph
        for value in self.module.__dict__.values():
            if callable(value) and hasattr(value, "is_step"):
                # check the next value and add it as edge
                click.secho(value.name, fg="green")
                click.secho(value.__doc__, fg="bright_red")
                click.secho(f"==>Next Callable: {value.next}\n", fg="blue")

        # traverse the graph
        # iterate over graph
            # echo the index '0 level'
            # iterate over function
                # echo function
                # echo next



    def _create_graph(self):
        # start will always be the start
        #start_nodeself.start
        next_node_list = None
        # iterate over nodes in start
        current_node = []
        for node in self.start:
            temp_next = self.node_func_map[node].next
            next_node_list.append(*temp_next,)
        print(current_node)
            # for each of them get their next value through node_func_map
            # add the next as list value
        # for each of the next in self.graph
        # while their next is not None
            # for next in
        pass

    def validate_graph(self):
        """This method should make sure
        that the graph is valid

        Scenarios to check:
        - next is None and that function is not @end
        - next is not present in list of functions
        - start function is present as a next function
        """
        pass

    @staticmethod
    def _create_graph_node(func):
        """Static method to create
        nodes for graph"""
        if isinstance(func.next, list):
            return {func.name: [func for func in func.next]}
        else:
            return {func.name: func.next}




def run_flow():
    pass