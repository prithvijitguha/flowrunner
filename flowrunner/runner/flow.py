"""This module contains two main exposed classes
to uses
BaseFlow: A base class to build flows off of
FlowRunner: A class to run any subclass of BaseFlow
"""
from flowrunner.system.logger import logger
from flowrunner.core.base import GraphOptions, Graph
from flowrunner.core.helpers import GraphValidator
from dataclasses import dataclass, field
import click


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

    @classmethod
    def show(cls):
        """Class method to show nodes/levels"""
        FlowRunner(cls).show()

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

    def show(self):
        """Method to show flow"""
        # we iterate through the functions level wise and we store the
        # output into a datastore
        for level in self.graph.levels:
            for node in level:
                click.secho(node.name, bg="bright_red")
                if node.next:
                    click.secho(node.next, bg="green")
