# -*- coding: utf-8 -*-
"""This module contains two main exposed classes
to uses
BaseFlow: A base class to build flows off of
FlowRunner: A class to run any subclass of BaseFlow
"""
from dataclasses import dataclass, field

import click

from flowrunner.core.base import Graph, GraphOptions
from flowrunner.core.helpers import GraphValidator
from flowrunner.system.logger import logger


@dataclass
class BaseFlow:
    """BaseFlow is the base class on which all flows are
    derived from

    Attributes:
        - data_store: A dict that is meant to be used to store data in key:value pairs
    """

    data_store: dict = field(default_factory=lambda: dict())

    @classmethod
    def validate(cls):
        """Class method to validate the graph"""
        FlowRunner(cls).validate()

    @classmethod
    def validate_with_error(cls):
        """Class method to validate the graph"""
        FlowRunner(cls).validate_with_error()

    @classmethod
    def run(cls):
        """Class Method to run flow"""
        FlowRunner(cls).validate_with_error()  # we run this in case of an invalid flow
        FlowRunner(cls).run()

    @classmethod
    def show(cls):
        """Class method to show nodes/levels"""
        FlowRunner(cls).validate()
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
        self.flow_name = self.base_flow.__name__
        graph_options = GraphOptions(self.base_flow)
        self.graph_instance = (
            graph_options.base_flow_instance
        )  # we store the same graph instance attribute of GraphOptions
        self.graph = Graph(graph_options=graph_options)

    def validate(self):
        """Method to run validations on a BaseFlow subclass"""
        logger.debug("Validating flow for %s", self.flow_name)
        graph_validator = GraphValidator(self.graph)
        graph_validator.run_validations()

    def validate_with_error(self):
        """Method to run validations on a BaseFlow subclass"""
        logger.debug("Validating flow for %s", self.flow_name)
        logger.warning(
            "Validation will raise InvalidFlowException if invalid Flow found"
        )
        graph_validator = GraphValidator(self.graph)
        graph_validator.run_validations_raise_error()

    def run(self):
        """Method to run any BaseFlow subclass"""
        logger.debug("Running flow for %s", self.flow_name)
        # we iterate through the functions level wise and we store the
        # output into a datastore
        for level in self.graph.levels:
            for node in level:
                node.function_reference(self.graph_instance)

    def show(self):
        """Method to show flow"""
        logger.debug("Show flow for %s", self.flow_name)
        # iterate through graph levels
        for level in self.graph.levels:
            # iterate through each node in the list
            for node in level:
                click.secho(f"{node.name}\n", fg="green")  # echo the node
                docstring = (
                    node.docstring or "?"
                )  # echo the docstring if docstring is None then echo "?"
                click.secho(docstring, fg="bright_red")
                next_callables = ", ".join(node.next)
                click.secho(f"   Next={next_callables}\n\n", fg="blue")
