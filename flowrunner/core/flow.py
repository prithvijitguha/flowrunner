from flowrunner.system.logger import logger
from dataclasses import dataclass, field
from typing import Any
import click

from flowrunner.system.exceptions import InvalidFlowException


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







@dataclass
class BaseFlow:
    """BaseFlow is the base class on which all flows are
    derived from

    Attributes:
        - data_store: A dict that is meant to be used to store data in key:value pairs
    """
    data_store: dict = field(default_factory=lambda: dict())
    @classmethod
    def validate_flow(cls):
        """Class method to validate the graph"""
        FlowRunner(cls).run_validations()

    @classmethod
    def validate_flow_with_error(cls):
        """Class method to validate the graph"""
        FlowRunner(cls).run_validations_raise_error()

    @classmethod
    def run_flow(cls):
        """Class Method to run flow"""
        FlowRunner(cls).run_flow()


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
    base_flow: BaseFlow
    functions: dict = field(default_factory=lambda: dict())
    middle_nodes: list = field(default_factory=lambda: list())
    start: list = field(default_factory=lambda: list())
    end: list = field(default_factory=lambda: list())

    def __post_init__(self):
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


@dataclass
class GraphValidator:
    """This class is used to validate any Graph
    It checks for the following:
    - There should be atleast 1 start
    - There should be atleast 1 end
    - There should be atleast 1 middle
    - All start nodes have a next value
    - All middle nodes have a next value
    - No end nodes have a next value
    - Any step that is not a next for any function
    - Any start function that is mentioned in another next
    - Validate each node, makes sure it has a return statement at the end
    """

    graph: Graph

    def validate_length_start_nodes(self) -> tuple[bool, str]:
        # check that the len of start is more than 1
        if len(self.graph.start) == 0:
            return (False, "No start nodes present, please specify with '@start'")
        return (True, "Validated number of start nodes")

    def validate_start_next_nodes(self) -> tuple[bool, str]:
        # check that all the start have a next value
        # All start nodes have a next value
        bad_start_nodes = []
        for start_node in self.graph.start:
            if not start_node.function_reference.next:
                bad_start_nodes.append(start_node.name)
        if bad_start_nodes:
            return (False, f"Nodes {bad_start_nodes} do not have next")
        return (True, "Validated start nodes 'next' values")

    def validate_length_middle_nodes(self) -> tuple[bool, str]:
        # check that the len of start is more than 1
        if len(self.graph.middle_nodes) == 0:
            return (
                False,
                "No middle_nodes present, please specify with '@step' and without '@start' or '@end'",
            )
        return (True, "Validate number of middle_nodes")

    def validate_middle_next_nodes(self) -> tuple[bool, str]:
        # check that all the start have a next value
        # All start nodes have a next value
        bad_middle_nodes = []
        for middle_node in self.graph.middle_nodes:
            if not middle_node.function_reference.next:
                bad_middle_nodes.append(
                    middle_node.name
                )  # append the node to bad nodes for later
        # if bad nodes has a length then we assume a failure
        if bad_middle_nodes:
            return (False, f"Nodes {bad_middle_nodes} do not have next")
        return (True, "Validated middle_nodes 'next' values")

    def validate_length_end_nodes(self) -> tuple[bool, str]:
        # check that the len of start is more than 1
        if len(self.graph.end) == 0:
            return (False, "No end present, please specify with '@end'")
        return (True, "Validated end nodes")

    def validate_end_nodes_no_next(self) -> tuple[bool, str]:
        # check that all the start have a next value
        # All start nodes have a next value
        bad_end_nodes = []
        for end_node in self.graph.end:
            if end_node.function_reference.next:
                bad_end_nodes.append(end_node.name)
        if bad_end_nodes:
            return (
                False,
                f"Nodes {bad_end_nodes} have next, end nodes cannot have 'next' value",
            )
        return (True, "Validated start nodes 'next' values")

    def get_validation_suite(self):
        """Define validation suite, more methods
        need to be added to validation suite list
        """
        validation_suite = [
            self.validate_length_start_nodes,
            self.validate_start_next_nodes,
            self.validate_length_middle_nodes,
            self.validate_middle_next_nodes,
            self.validate_length_end_nodes,
            self.validate_end_nodes_no_next,
        ]
        return validation_suite

    def run_validations(self):
        """Method to run all validation methods
        We iterate through the validation suite for each method and check
        the output. Output is always in the form of Tuple[bool, str]. With bool for Pass or
        Fail and str being the output message
        """
        validation_suite = self.get_validation_suite()

        # iterate through the list of validations
        for validation in validation_suite:
            result, message = validation()  # run the validation and check the output
            if result == True:
                click.secho(f"✅ {message}", fg="green")
            elif result == False:
                click.secho(f"❌ {message}", fg="bright_red")

    def run_validations_raise_error(self):
        """Method to run all validation methods but we raise an error if anything fails
        We iterate through the validation suite for each method and check
        the output. Output is always in the form of Tuple[bool, str]. With bool for Pass or
        Fail and str being the output message
        """
        validation_suite = self.get_validation_suite()

        validation_output = []  # a list to store the values of the output

        # iterate through the list of validations
        for validation in validation_suite:
            result, message = validation()  # run the validation and check the output
            validation_output.append(result)
            if result == True:
                click.secho(f"✅ {message}", fg="green")
            elif result == False:
                click.secho(f"❌ {message}", fg="bright_red")

        if all(validation_output) != True:
            raise InvalidFlowException("Invalid Flow detected")


@dataclass
class FlowRunner:
    """FlowRunner class is used to run all subclasses of BaseFlow class.
    Attributes:
        - base_flow: A subclass of BaseFlow
        - graph_instance: An instance of self.base_flow, assigned in __post_init__
        - graph: A Graph object constructed from self.base_flow, assigned in __post_init__
    """

    base_flow: BaseFlow

    def __post_init__(self):
        """A method done after instance of FlowRunner is created to generate the graph and arrange it"""
        graph_options = GraphOptions(self.base_flow)
        self.graph_instance = (
            graph_options.base_flow_instance
        )  # we store the same graph instance attribute of GraphOptions
        self.graph = Graph(graph_options=graph_options)
        self.graph._arrange_graph()

    def run_validations(self):
        """Method to run validations on a BaseFlow subclass"""
        graph_validator = GraphValidator(self.graph)
        graph_validator.run_validations()

    def run_validations_raise_error(self):
        """Method to run validations on a BaseFlow subclass"""
        graph_validator = GraphValidator(self.graph)
        graph_validator.run_validations_raise_error()

    def run_flow(self):
        """Method to run any BaseFlow subclass"""
        # we iterate through the functions level wise and we store the
        # output into a datastore
        for level in self.graph.levels:
            for node in level:
                node.function_reference(self.graph_instance)

    def show_flow(self):
        """Method to show flow"""
        # we iterate through the functions level wise and we store the
        # output into a datastore
        pass
