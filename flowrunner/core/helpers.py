# -*- coding: utf-8 -*-
"""Modules for any helpers for any base.py classes

GraphValidator: A class for validating any subclass of BaseFlow
"""


import os
from dataclasses import dataclass

import click
from jinja2 import Environment, FileSystemLoader

from flowrunner.runner.flow import Graph
from flowrunner.system.exceptions import InvalidFlowException
from flowrunner.system.logger import logger


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

    Each of the method represents a seperate check of the validation suite to be conducted on the self.graph attribute.
    All the methods a tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
    of the output message.

    Attributes:
        - graph: An instance of Graph class to be checked
    """

    graph: Graph

    def validate_length_start_nodes(self) -> tuple[bool, str]:
        """Method to validate the length of start nodes.

        We make sure that there is atleast one start node

        Args:
            - None

        Returns:
            - A tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
                of the output message.
        """
        # check that the len of start is more than 1
        if len(self.graph.start) == 0:
            return (False, "No start nodes present, please specify with '@start'")
        return (True, "Validated number of start nodes")

    def validate_start_next_nodes(self) -> tuple[bool, str]:
        """Method to check that the start nodes specified are valid.

        We make sure that each of the nodes specified has a next

        Args:
            - None

        Returns:
            - A tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
                of the output message
        """
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
        """Method to validate the length of middle nodes.

        We make sure that there is atleast one start node

        Args:
            - None

        Returns:
            - A tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
                of the output message.
        """
        # check that the len of start is more than 1
        if len(self.graph.middle_nodes) == 0:
            return (
                False,
                "No middle_nodes present, please specify with '@step' and without '@start' or '@end'",
            )
        return (True, "Validate number of middle_nodes")

    def validate_middle_next_nodes(self) -> tuple[bool, str]:
        """Method to check that the middle nodes specified are valid.

        We make sure that each of the nodes specified has a next

        Args:
            - None

        Returns:
            - A tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
                of the output message
        """
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
        """Method to validate the length of end nodes.

        We make sure that there is atleast one end node

        Args:
            - None

        Returns:
            - A tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
                of the output message.
        """
        # check that the len of start is more than 1
        if len(self.graph.end) == 0:
            return (False, "No end present, please specify with '@end'")
        return (True, "Validated end nodes")

    def validate_end_nodes_no_next(self) -> tuple[bool, str]:
        """Method to check that the end nodes specified are valid.

        We make sure that each of the nodes specified does have a next value

        Args:
            - None

        Returns:
            - A tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
                of the output message
        """
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

        Any new validation method has to be added to validation_suite so that it can
        be called on validation checks.

        Args:
            - None

        Returns:
            - validation_suite: A dict object containing the list of GraphValidator methods to be used to validate
                base_flow subclasses
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

    def run_validations(self, terminal_output: bool = True):
        """Method to run all validation methods
        We iterate through the validation suite for each method and check
        the output. Output is always in the form of Tuple[bool, str]. With bool for Pass or
        Fail and str being the output message

        Args:
            - terminal_output: An optional bool argument for whether to show the output in terminal

        Returns:
            - Echo of output {✅} or {❌} if passed or failed respectively with message
        """
        validation_suite = self.get_validation_suite()

        # iterate through the list of validations
        for validation in validation_suite:
            result, message = validation()  # run the validation and check the output
            if result == True and terminal_output:
                click.secho(f"✅ {message}", fg="green")
            elif result == False and terminal_output:
                click.secho(f"❌ {message}", fg="bright_red")

    def run_validations_raise_error(self, terminal_output: bool = True):
        """Method to run all validation methods but we raise an error if anything fails
        We iterate through the validation suite for each method and check
        the output. Output is always in the form of Tuple[bool, str]. With bool for Pass or
        Fail and str being the output message

        Args:
            - terminal_output: An optional bool argument for whether to show the output in terminal

        Returns:
            - Echo of output {✅} or {❌} if passed or failed respectively with message

        Raises:
            - InvalidFlowException: If any validation check failed
        """
        validation_suite = self.get_validation_suite()

        validation_output = []  # a list to store the values of the output

        # iterate through the list of validations
        for validation in validation_suite:
            result, message = validation()  # run the validation and check the output
            validation_output.append(result)
            if result == True and terminal_output:
                click.secho(f"✅ {message}", fg="green")
            elif result == False and terminal_output:
                click.secho(f"❌ {message}", fg="bright_red")

        if all(validation_output) != True:
            raise InvalidFlowException("Invalid Flow detected")


class FlowChartGenerator:
    """Class to build html flowcharts from graphs"""

    @classmethod
    def _create_flowchart(cls, flow_instance):
        """Class method to create the base graph for mermaid js

        We iterate over the Graph.levels to understand the order of iteration. Then
        we find the 'next' of each to make the edge connections. The final string should look like:

        Examples:
            >>> FlowChartGenerator()._create_flowchart(flow_instance)
            graph TD;
                create_data(create_data)==>transformation_function_1(transformation_function_1)
                create_data(create_data)==>transformation_function_2(transformation_function_2)
                transformation_function_2(transformation_function_2)==>append_data(append_data)
                transformation_function_1(transformation_function_1)==>append_data(append_data)
                append_data(append_data)==>show_data(show_data)

        Args:
            flow_instance: An instance of BaseFlow

        Returns:
            mermaid_js_string: A string render of the javascript string for mermaid js
        """
        graph = flow_instance.graph  # get the graph attribute which is Graph object
        mermaid_js_string = (
            "graph TD;\n"  # this will be passed to mermaid-js for rendering
        )
        # iterate through graph levels
        for level in graph.levels:
            # iterate through each node in the list of levels [node1, node2]
            for node in level:  # each node is an actual Node object
                for next_node in node.next:
                    # edge string represents a connection in mermaid js
                    edge_string = f"    {node.name}({node.name})==>{next_node}({next_node})\n"  # this will look create_data(create_data)==>transformation_function_2(transformation_function_2)
                    mermaid_js_string += edge_string

        return mermaid_js_string

    @classmethod
    def generate_html(cls, flow_instance, save_file: False):
        """Class method to generate html output from a BaseFlow instance

        We use the templates/base.html to create the flow html diagram.

        Args:
            flow_instance: An instance of BaseFlow subclass object
            save_file: Bool value to save file, defaults to False

        Returns:
            content: The html data containing the flow diagram
        """
        mermaid_js_string = cls._create_flowchart(flow_instance=flow_instance)

        root = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(root, "templates")
        environment = Environment(
            loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True
        )
        template = environment.get_template("base.html")

        flow_name = flow_instance.__class__.__name__  # Output eg.'ExamplePandas'

        filename = f"{flow_name.lower()}.html"  # Output eg. examplepandas.html

        content = template.render(
            flow_name=flow_name, mermaid_js_string=mermaid_js_string
        )

        if save_file:  # save_file is bool argument
            with open(filename, mode="w", encoding="utf-8") as message:
                logger.debug("Saving file: %s", filename)
                message.write(content)
                logger.debug("Saved file %s", filename)

        return content

    def display(cls, flow_instance):
        """Class method to display the html data"""
        raise NotImplementedError
