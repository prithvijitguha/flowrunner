# -*- coding: utf-8 -*-
"""Module with base classes for use in other modules

Node: A class for containing functions, with the function name, actual function reference, docstring and its next functions
GraphOptions: A class for all the options to be given to Graph, a collection of start, middle and end nodes
Graph: A class containing an arranged collection of Nodes from start, middle, end in Graph.levels
"""
from dataclasses import dataclass
from typing import Type


@dataclass
class Node:
    """A class for containing functions, with the function name, actual function reference, docstring and
    its next functions

    Attributes:
        name: A str value of the name of the function __name__
        function_reference: The actual function or callable
        next: None by default, list value of what is next node, assigned in __post_init__
        docstring: Docstring of method assigned in __post_init__
    """

    name: str
    function_reference: callable

    def __post_init__(self):
        """In post init we get the next node if
        its present.

        We make sure that 'next' keyword argument is passed as either a single 'str' or 'list'. If
        next is None then we just assign an empty list as 'next' attribute

        Args:
            - None

        Returns:
            - None

        Raises:
            - If more than 1 type of element found in 'next' keyword argument. Only a single string referencing a
                function or a list of strings referencing functions are accepted
        """
        # store the __doc__ as attribute docstring
        self.docstring = self.function_reference.__doc__
        # if next has value
        if self.function_reference.next:
            if isinstance(self.function_reference.next, list):
                # iterate over each elment in the list and peform checks on them
                # we stop these errors at Node level as they can break the GraphOptions and Graph objects
                for next_node in self.function_reference.next:
                    if not isinstance(next_node, str): # if its not string raise a Type Error
                        raise TypeError(f"Elements of 'next' can only be 'str' type, found {type(next_node)} for {next_node}")
                    if self.function_reference.next.count(next_node) > 1: # if the count it means its a duplicate next node
                        raise ValueError(
                        f"'next' values are not unique, got duplicate values for '{next_node}'"
                        )

                self.next = self.function_reference.next
            elif isinstance(self.function_reference.next, str):
                # we make sure that the next is put in a list
                print(self.function_reference.next)
                self.next = [self.function_reference.next]

            else: # We do not allow any other types other than list and str
                raise TypeError(
                        f"'next' value can only be 'list of str' or 'str', found: {type(self.function_reference.next)}"
                    )
        else:
            self.next = []

        # check if method name in next is same as current
        if self.next:  # only if next list if full. ie. Only for start and middle
            bad_next_list = [
                next_callable
                for next_callable in self.function_reference.next
                if self.name == next_callable
            ]
            if bad_next_list:
                raise ValueError(
                    f"Value for next cannot be same as method {self.name}.next={bad_next_list}"
                )

    def __repr__(self):
        """String representation of this node, which will be actual function
        name

        Args:
            - None

        Returns:
            - A string representation of the Node instance

        Examples:
            >>> node_example Node('some_func', some_func)
            some_func
        """
        return self.name

    def __hash__(self):
        """Method to make sure we hash on the function/method name
        We expect the function/method names to be unique
        """
        return hash(self.name)


# class to handle the seperation of functions
@dataclass
class GraphOptions:
    """A class for all the options to be given to Graph, a collection of start, middle and end nodes

    We only take base_flow argument, the rest of the attributes are assigned in the __post_init__. We iterate over
    all the methods in the class and arrange them according to 'start', 'step', 'end' as per the decorators.

    Attributes:
        - base_flow: A subclass of BaseFlow
        - functions: A dictionary of {'test_1': <function Test.test_1 at 0x000002390259E9D0>} using inbuilt __dict__ method
        - middle_nodes: A list of middle nodes i.e methods with only 'step' and no 'start' and 'end' decorator
        - start: A list of middle nodes i.e methods with 'start' decorator
        - end: A list of middle nodes i.e methods with 'end' decorator
        - base_flow_instance: An instance of base_flow we use later to run flows
    """

    # list of functions/module
    base_flow: Type

    def __post_init__(self):
        """Method to assign some attributes for the BaseFlow.

        We assign the following attributes

        Attributes:
            - functions: A dictionary of {'test_1': <function Test.test_1 at 0x000002390259E9D0>} using inbuilt __dict__ method
            - middle_nodes: A list of middle nodes i.e methods with only 'step' and no 'start' and 'end' decorator
            - start: A list of middle nodes i.e methods with 'start' decorator
            - end: A list of middle nodes i.e methods with 'end' decorator
            - base_flow_instance: An instance of base_flow we use later to run flows

        Args:
            - None

        Returns:
            - A string representation of the class

        Examples:
            >>> print(graph_options_instance)
            Start=['method_1']
            Middle Nodes=['method_2']
            End=['method_3']

        """
        self.functions = (
            self.base_flow.__dict__
        )  # returns a dict of method name and actual reference {'test_1': <function Test.test_1 at 0x000002390259E9D0>}
        self.middle_nodes = (
            []
        )  # list to store any methods that have 'step' decorator but NO 'start' or 'end'
        self.start = []  # list to store any methods that have 'start' decorator
        self.end = []  # list to store any methods that have 'end' decorator

        # iterate over list of functions/methods of the class, we do a check to make sure that it is a callable.
        # if it is a callable we make distinctions based on attributes. 'is_step', 'is_end' and 'is_start'. Following conditions classify them
        # IF 'is_step' NO 'is_start' NO 'is_end' THEN 'middle_nodes'
        # IF 'is_step' YES 'is_start' NO 'is_end' THEN 'start'
        # IF 'is_step' NO 'is_start' YES 'is_end' THEN 'end'
        for name_func, func in self.functions.items():
            if callable(func):
                # we check if it has 'is_step' in the attribute
                # then we do other checks on it
                if hasattr(func, "is_step"):
                    if hasattr(func, "is_start") and not hasattr(func, "is_end"):  # IF 'is_step'== YES 'is_start'== NO 'is_end' THEN 'start'
                        self.start.append(Node(name_func, func))

                    elif not hasattr(func, "is_start") and not hasattr(func, "is_end"): # IF 'is_step'== YES AND 'is_start' NO 'is_end' == NO THEN 'middle_nodes'
                        self.middle_nodes.append(Node(name_func, func))

                    elif hasattr(func, "is_start") and hasattr(func, "is_end"): # edge case if has step and start and end
                        raise ValueError(f"Not cannot have both start and end, {func}")

                    elif hasattr(func, "is_end") and not hasattr(func, "is_start"):  # IF 'is_step' == YES AND 'is_end'==YES THEN 'end'
                        self.end.append(Node(name_func, func))
                        if func.next:
                            raise ValueError(f"End nodes cannot have next attribute {func}") # check if there is next attribute, if it is, then raise an error



    def __repr__(self):
        """String representation of class
        Args:
            None

        Returns:
            A string representation of the GraphOptions instance

        Examples:
            >>> print(graph_options_instance)
            Start=['method_1']
            Middle Nodes=['method_2']
            End=['method_3']

        """
        return f"Start={self.start}\nMiddle Nodes={self.middle_nodes}\nEnd={self.end}"


@dataclass
class Graph:
    """A class containing an arranged collection of Nodes from start, middle, end in Graph.levels

    Attributes:
        graph_options: An instance of GraphOptions class
        start: A list of start nodes, we take this from GraphOptions.start, A list of nodes decorated with @start
        middle_nodes: A list of middle nodes, we take this from GraphOptions.middle_nodes, A list of nodes decorated with @step only
        end: A list of end nodes, we take this from GraphOptions.end, A list of nodes decorated with @end
        nodes: A list of all the nodes start + middle_nodes + end
        node_map: A dict of {node.name: node} for reference for later
        levels: A list containing the iteration order for methods from start -> middle_nodes -> end
    """

    graph_options: GraphOptions

    def __post_init__(self):
        """Method to arrange the start, middle and end nodes.

        In addition to arranging the nodes as per their order of iteration

        Graph.levels = [
            ['method_1'], # start nodes
            ['method_2', 'method_3'], # middle nodes
            ['method_4'] # end nodes
        ]
        In addition, we assign the following attributes.

        Attributes:
            start: A list of start nodes, we take this from GraphOptions.start, A list of nodes decorated with @start
            middle_nodes: A list of middle nodes, we take this from GraphOptions.middle_nodes, A list of nodes decorated with @step only
            end: A list of end nodes, we take this from GraphOptions.end, A list of nodes decorated with @end
            nodes: A list of all the nodes start + middle_nodes + end
            node_map: A dict of {node.name: node} for reference for later

        Args:
            None

        Returns:
            None
        """
        self.start = self.graph_options.start
        self.middle_nodes = self.graph_options.middle_nodes
        self.end = self.graph_options.end
        self.nodes = self.start + self.middle_nodes + self.end
        self.node_map = {node.name: node for node in self.nodes}
        self.levels = []
        self._arrange_graph()

    def _arrange_graph(self):
        """Method to arrange the Nodes in the Graph into the order of iteration

        We assume that start will be the root node, after that we iterate over the next of each
        node and append them to each level.

        Args:
            None

        Returns:
            None
        """
        # TODO: Maybe in the future there may be a need to add 'end' node or a later node in 'middle_nodes' to the 'next' of 'start'. Need to add
        # check to remove any function in end and mentioned in middle nodes
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
