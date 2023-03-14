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

    def validate(self, terminal_output: bool = False):
        """Class method to validate the graph"""
        FlowRunner().validate(flow_instance=self, terminal_output=terminal_output)

    def validate_with_error(self, terminal_output: bool = False):
        """Class method to validate the graph"""
        FlowRunner().validate_with_error(
            flow_instance=self, terminal_output=terminal_output
        )

    def run(self):
        """Class Method to run flow"""
        FlowRunner().validate_with_error(
            flow_instance=self, terminal_output=False
        )  # we run this in case of an invalid flow
        FlowRunner().run(flow_instance=self)

    def show(self):
        """Class method to show nodes/levels"""
        FlowRunner().validate(flow_instance=self, terminal_output=False)
        FlowRunner().show(flow_instance=self)


@dataclass
class FlowRunner:
    """FlowRunner class is used to run all subclasses of BaseFlow class.
    Attributes:
        - base_flow: A subclass of BaseFlow
        - graph_instance: An instance of self.base_flow, assigned in __post_init__
        - graph: A Graph object constructed from self.base_flow, assigned in __post_init__
    """

    def _get_details(cls, flow_instance):
        """A method done after instance of FlowRunner is created to generate the graph and arrange it"""
        base_flow = flow_instance.__class__
        graph_options = GraphOptions(base_flow)
        # self.graph_instance = (
        #     graph_options.base_flow_instance
        # )  # we store the same graph instance attribute of GraphOptions
        graph = Graph(graph_options=graph_options)
        return graph

    @classmethod
    def validate(cls, flow_instance, terminal_output: bool = False):
        """Method to run validations on a BaseFlow subclass"""
        logger.debug("Validating flow for %s", flow_instance)
        graph = cls._get_details(cls=cls, flow_instance=flow_instance)
        graph_validator = GraphValidator(graph)
        graph_validator.run_validations(terminal_output=terminal_output)

    @classmethod
    def validate_with_error(cls, flow_instance, terminal_output: bool = False):
        """Method to run validations on a BaseFlow subclass"""
        logger.debug("Validating flow for %s", flow_instance)
        logger.warning(
            "Validation will raise InvalidFlowException if invalid Flow found"
        )
        graph = cls._get_details(cls=cls, flow_instance=flow_instance)
        graph_validator = GraphValidator(graph)
        graph_validator.run_validations_raise_error(terminal_output=terminal_output)

    @classmethod
    def run(cls, flow_instance):
        """Method to run any BaseFlow subclass"""
        logger.debug("Running flow for %s", flow_instance)
        graph = cls._get_details(cls=cls, flow_instance=flow_instance)
        # we iterate through the functions level wise and we store the
        # output into a datastore
        for level in graph.levels:
            for node in level:
                output = node.function_reference(
                    flow_instance
                )  # store the output of the method

                flow_instance.data_store[
                    node.name
                ] = output  # we add it to the instance data_store = {'function_name_1': df}

    @classmethod
    def show(cls, flow_instance):
        """Method to show flow"""
        logger.debug("Show flow for %s", flow_instance)
        graph = cls._get_details(cls=cls, flow_instance=flow_instance)
        # iterate through graph levels
        for level in graph.levels:
            # iterate through each node in the list
            for node in level:
                click.secho(f"{node.name}\n", fg="green")  # echo the node
                docstring = (
                    node.docstring or "?"
                )  # echo the docstring if docstring is None then echo "?"
                click.secho(docstring, fg="bright_red")
                next_callables = ", ".join(node.next)
                click.secho(f"   Next={next_callables}\n\n", fg="blue")
