from dataclasses import dataclass
from typing import Type

@dataclass
class Node:
    """A class that contains the node object
    Attributes:
        name: A str value of the name of the function __name__
        function_reference: The actual function or callable
        next: None by default, list value of what is next node, assigned in __post_init__
        doc: Docstring of method assigned in __post_init__
    """

    name: str
    function_reference: callable

    def __post_init__(self):
        """In post init we get the next node if
        it is there"""
        # store the __doc__ as attribute docstring
        self.docstring = self.function_reference.__doc__
        # if next has value
        if self.function_reference.next:
            if isinstance(self.function_reference.next, list):
                # we do a check to see that all elements in the list
                # are a string
                element_types = [
                    type(element) for element in self.function_reference.next
                ]
                elements_unique = list(set(element_types))
                # we make sure that the types are uniform
                # if the len of the set is more than 1 then we raise an error
                if len(elements_unique) > 1:
                    raise TypeError(
                        f"More than 1 type of element found, next can be str or list of str, found: {elements_unique}"
                    )
                # if all the elements are uniform, we make sure that
                # they are all of string type
                if isinstance(type(elements_unique[0]), str):
                    raise TypeError(
                        f"'next' value can only be 'list of str' or 'str', found: {type(elements_unique[0])}"
                    )
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
        - functions: A
    """

    # list of functions/module
    base_flow: Type
    def __post_init__(self):
        self.functions= {}
        self.middle_nodes = []
        self.start = []
        self.end = []
        # if module get the list of functions
        if not isinstance(self.base_flow, list):
            self.functions = self.base_flow.__dict__
        # if list of functions directly iterate over them
        elif isinstance(self.base_flow, list):
            self.functions = {func.__name__: func for func in self.base_flow}

        # iterate over list of functions
        # find the start
        # find the end
        for name_func, func in self.functions.items():
            if callable(func):
                # the ones with step, start and end in them
                if (
                    hasattr(func, "is_step")
                    and not hasattr(func, "is_start")
                    and not hasattr(func, "is_end")
                ):
                    self.middle_nodes.append(Node(name_func, func))
                elif hasattr(func, "is_step") and hasattr(func, "is_start"):
                    self.start.append(Node(name_func, func))
                elif hasattr(func, "is_step") and hasattr(func, "is_end"):
                    self.end.append(Node(name_func, func))

        # store an instance of the class that
        # we are running
        self.base_flow_instance = self.base_flow()

    def __repr__(self):
        return f"Start={self.start}\nMiddle Nodes={self.middle_nodes}\nEnd={self.end}"




@dataclass
class Graph:
    """Graph is a class that stores the graph object, classify nodes
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
        self._arrange_graph()

    def _arrange_graph(self):
        """Method to traverse graph and arrange into
        self.levels and self.edges
        """
        # create temp_node = start
        temp_level = self.start

        self.levels.append(temp_level)  # add temp level to 'self.levels'

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
            next_level = list(
                set(next_level)
            )  # we make sure the nodes in the level are unique
            if not next_level:
                break
            self.levels.append(next_level)
            temp_level = next_level

    def generate_html(self):
        """A method to generate the html graph using go-js"""
        pass



