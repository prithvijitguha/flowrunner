from dataclasses import dataclass, field
from flowrunner.core.data_store import _DataStore
from typing import Any


_datastore = _DataStore()

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

    def __post_init__(self):
        """In post init we get the next node if
        it is there"""
        # if next has value
        if self.function_reference.next:
            if isinstance(self.function_reference.next, list):
                # we do a check to see that all elements in the list
                # are a string
                element_types = [type(element) for element in self.function_reference.next]
                elements_unique = list(set(element_types))
                # we make sure that the types are uniform
                # if the len of the set is more than 1 then we raise an error
                if len(elements_unique) > 1:
                    raise TypeError(f"More than 1 type of element found, next can be str or list of str, found: {elements_unique}")
                # if all the elements are uniform, we make sure that
                # they are all of string type
                if isinstance(type(elements_unique[0]), str):
                    raise TypeError(f"'next' value can only be 'list of str' or 'str', found: {type(elements_unique[0])}")
                # then we assign the next
                self.next = self.function_reference.next
            elif isinstance(self.function_reference.next, str):
                # we make sure that the next is put in a list
                self.next = [self.function_reference.next]
        else:
            self.next = []

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

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
        self.levels = []


    def validate_graph(self):
        """Method to validate any graph. Things to check for
        - There should be atleast 1 start
        - There should be atleast 1 end
        - There should be atleast 1 middle
        - All start nodes have a next value
        - All middle nodes have a next value
        - Any step that is not a next for any function
        - Any start function that is mentioned in another next
        - An end that has a next value
        - Validate each node
        """
        pass


    def _arrange_graph(self):
        """Method to traverse graph and arrange into
        self.levels and self.edges
        """
        # create temp_node = start
        temp_level = self.start

        self.levels.append(temp_level) # add temp level to 'self.levels'

        # while loop for when temp_level is not empty
        while temp_level:
            next_level = []
            # iterate through temp node
            # find the next of each
            for node in temp_level:
                # we iterate through the list of 'node.next' and
                # using the 'self.node_map' we find the Node
                next = [self.node_map[next_node] for next_node in node.next]
                # add the next to the list
                next_level += next
            next_level = list(set(next_level))# we make sure the nodes in the level are unique
            if not next_level:
                break
            self.levels.append(next_level)
            temp_level = next_level

        print(self.levels)

    def generate_html(self):
        """A method to generate the html page"""
        pass

    def run_flow(self):
        """A method to run the graph
        To run the flow we iterate over 'self.levels'
        and we call each function"""
        for level in self.levels:
            for node in level:
                function_output = node.function_reference()
                _datastore[node.name] = function_output





@dataclass
class BaseFlow:
    def read_output(self, method_name: str):
        """Method to read output of another method"""
        pass
