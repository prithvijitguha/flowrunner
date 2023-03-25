# -*- coding: utf-8 -*-
"""This module contains two main exposed classes
to uses
BaseFlow: A base class to build flows off of
FlowRunner: A class to run any subclass of BaseFlow
"""
from dataclasses import dataclass, field

import click

from flowrunner.core.base import Graph, GraphOptions
from flowrunner.core.helpers import DAGGenerator, GraphValidator
from flowrunner.system.logger import logger


@dataclass
class BaseFlow:
    """BaseFlow is the base class on which all flows are
    derived from

    These are not meant to be used directly, but subclass/parent class for any Flow

    Attrs:
        data_store: A dict that is meant to be used to store data by method name and output eg. {'dataframe1': DataFrame}.
        param_store: A dict that stores parameter values eg. {'snapshot_date': '2023-01-01}.

    """

    data_store: dict = field(default_factory=lambda: {}) # a way to store any data and output from methods if any
    param_store: dict = field(default_factory=lambda: {}) # a way to store any input params to the Flow

    def __post_init__(self):
        """Post init to add attributes like levels

        Args:
            None

        Returns:
            None: But we
        """
        graph = FlowRunner()._get_details(self)
        self.graph = graph

    def validate(self, terminal_output: bool = True):
        """Method to validate a flow

        We use the FlowRunner class to run the validation checks.

        Args:
            flow_instance: An instance of the Flow class
            terminal_ouput: An optional bool value of whether to display the terminal output
               for validate we choose to show the output, defaults to True
        Returns:
            None
        """
        FlowRunner().validate(flow_instance=self, terminal_output=terminal_output)

    def validate_with_error(self, terminal_output: bool = True):
        """Method to validate a flow with an error

        We use the FlowRunner class to run the validation checks.
        Args:
            flow_instance: An instance of the Flow class
            terminal_ouput: An optional bool value of whether to display the terminal output
               for validate we choose to show the output, defaults to True
        Returns:
            None

        Raises:
            InvalidFlowException: If an invalid flow is detected
        """
        FlowRunner().validate_with_error(
            flow_instance=self, terminal_output=terminal_output
        )

    def run(self):
        """Method to run a flow

        We first run a validation check with raise error and do not show the output. Then
        we use the FlowRunner class to run it

        Args:
            None
        Returns:
            None

        Raises:
            InvalidFlowException: If an invalid flow is detected
        """
        FlowRunner().validate_with_error(
            flow_instance=self, terminal_output=False
        )  # we run this in case of an invalid flow
        FlowRunner().run(flow_instance=self)

    def show(self):
        """Method to show the levels and order of iteration of the Flow

        We first run a validation check without raising an error and do not show the output. Then
        we use the FlowRunner class to run it

        Args:
            None

        Returns:
            None
        """
        FlowRunner().validate(flow_instance=self, terminal_output=False)
        FlowRunner().show(flow_instance=self)

    def display(self, description: bool = True):
        """Method to show html output of the flowchart

        Args:
            description: An optional bool argument which can turn off/on description. Defaults to True

        Returns:
            None: displays an html flowchart of the Flow

        """
        return DAGGenerator().display(flow_instance=self, description=description)

    def dag(self, save_file: bool = False, path: str = None, description: bool = True):
        """Method to generate html flowchart for Flow

        We first run a validation check without raising an error and do not show the output. Then
        we use the FlowRunner class to run it

        Args:
            save_file: Optional Bool value to save file or not
            path: Optional path to provide to save file, if path is provided, save_file is True implicitly

        Returns:
            content: HTMl data in the form of string
        """
        return DAGGenerator().dag(
            flow_instance=self, save_file=save_file, path=path, description=description
        )


@dataclass
class FlowRunner:
    """FlowRunner class is used to run all subclasses of BaseFlow class.

    We use class methods to run each of the flows
    """

    @classmethod
    def _get_details(cls, flow_instance):
        """Private class method to get details of a flow

        Args:
            flow_instance: An instance of the Flow class

        Returns:
            graph: A Graph object of the Flow

        Raises:
            InvalidFlowException: If an invalid flow is detected
        """
        base_flow = flow_instance.__class__
        graph_options = GraphOptions(base_flow)
        graph = Graph(graph_options=graph_options)
        return graph

    @classmethod
    def validate(cls, flow_instance, terminal_output: bool = False):
        """Class method to validate a Flow

        We use the GraphValidator to do the heavy lifting for this part

        Args:
            flow_instance: An instance of the Flow class
            terminal_output: An optional bool value to show output in terminal, defaults to False
        Returns:
            None

        """
        logger.debug("Validating flow for %s", flow_instance)
        graph = cls._get_details(flow_instance=flow_instance)
        graph_validator = GraphValidator(graph)
        graph_validator.run_validations(terminal_output=terminal_output)

    @classmethod
    def validate_with_error(cls, flow_instance, terminal_output: bool = False):
        """Class method to validate a Flow with an error

        We use the GraphValidator to do the heavy lifting for this part. We raise an error
        if validation check fails

        Args:
            flow_instance: An instance of the Flow class
            terminal_output: An optional bool value to show output in terminal, defaults to False

        Returns:
            None

        Raises:
            InvalidFlow: Raised if ANY of the validation checks are failed
        """
        logger.debug("Validating flow for %s", flow_instance)
        logger.warning(
            "Validation will raise InvalidFlowException if invalid Flow found"
        )
        graph = cls._get_details(flow_instance=flow_instance)
        graph_validator = GraphValidator(graph)
        graph_validator.run_validations_raise_error(terminal_output=terminal_output)

    @classmethod
    def run(cls, flow_instance):
        """Class method to run a Flow

        This method actually runs the flow and each method in order of iteration. We also do a validation
        check before we run it(without terminal output, just notification we are running it).
        During the run we iterate of Graph using the Graph.levels attribute, which is a list
            [
                [node1, node2], # first level
                [node3, node4]  # second level
            ]

        We also store the output of a function in that instance of the Flow, inside the attribute BaseFlow.data_store.

        eg. {
                'method_1': 7,
                'method_2': 8
            }

        Args:
            flow_instance: An instance of the Flow class

        Returns:
            None

        Raises:
            InvalidFlow: Raised if ANY of the validation checks are failed
        """
        logger.debug("Running flow for %s", flow_instance)
        graph = cls._get_details(flow_instance=flow_instance)
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
        """Class method to show a Flow

        This method we show the order of iteration by going over the levels in the Graph.levels attribute. This DOES NOT
        run the actual method but just uses the 'docstring' and '__name__' to show the Flow.

        Args:
            flow_instance: An instance of the Flow class

        Returns:
            None
        """
        logger.debug("Show flow for %s", flow_instance)
        graph = cls._get_details(flow_instance=flow_instance)
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
                if (
                    next_callables
                ):  # incase its end, we check if there is a next, if not we don't print 'Next='
                    click.secho(f"   Next={next_callables}\n\n", fg="blue")
