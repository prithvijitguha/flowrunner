# -*- coding: utf-8 -*-
"""Modules for any helpers for any base.py classes

GraphValidator: A class for validating any subclass of BaseFlow
DAGGenerator: A class for creating dags based on a subclass of BaseFlow
"""


import base64
import os
from dataclasses import dataclass
from typing import Tuple

import click
import matplotlib.pyplot as plt  # we have to import matplotlib so that we can use display()
from IPython.display import Image, display
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
    - Any step that is not a next for any function
    - Any start function that is mentioned in another next
    - Validate each node, makes sure it has a return statement at the end

    Each of the method represents a seperate check of the validation suite to be conducted on the self.graph attribute.
    All the methods a tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
    of the output message.

    Attributes:
        graph: An instance of Graph class to be checked
    """

    graph: Graph

    def validate_length_start_nodes(self) -> Tuple[bool, str]:
        """Method to validate the length of start nodes.

        We make sure that there is atleast one start node

        Args:
            None

        Returns:
            A tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
                of the output message.
        """
        # check that the len of start is more than 1
        if len(self.graph.start) == 0:
            return (False, "No start nodes present, please specify with '@start'")
        return (True, "Validated number of start nodes")

    def validate_start_next_nodes(self) -> Tuple[bool, str]:
        """Method to check that the start nodes specified are valid.

        We make sure that each of the nodes specified has a next

        Args:
            None

        Returns:
            A tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
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

    def validate_length_middle_nodes(self) -> Tuple[bool, str]:
        """Method to validate the length of middle nodes.

        We make sure that there is atleast one start node

        Args:
            None

        Returns:
            A tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
                of the output message.
        """
        # check that the len of start is more than 1
        if len(self.graph.middle_nodes) == 0:
            return (
                False,
                "No middle_nodes present, please specify with '@step' and without '@start' or '@end'",
            )
        return (True, "Validate number of middle_nodes")

    def validate_middle_next_nodes(self) -> Tuple[bool, str]:
        """Method to check that the middle nodes specified are valid.

        We make sure that each of the nodes specified has a next

        Args:
            None

        Returns:
            A tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
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

    def validate_length_end_nodes(self) -> Tuple[bool, str]:
        """Method to validate the length of end nodes.

        We make sure that there is atleast one end node

        Args:
            None

        Returns:
            A tuple of (test_result, output_message) where test_result will be a True/False bool and output_message is a string value
                of the output message.
        """
        # check that the len of start is more than 1
        if len(self.graph.end) == 0:
            return (False, "No end present, please specify with '@end'")
        return (True, "Validated end nodes")


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
            self.validate_length_end_nodes
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


class DAGGenerator:
    """Class to flowrunner DAGs based on Flow"""

    @classmethod
    def _create_dag(cls, flow_instance) -> str:
        """Class method to create the base graph for mermaid js

        We iterate over the Graph.levels to understand the order of iteration. Then
        we find the 'next' of each to make the edge connections. The final string should look like:

        Examples:
            >>> FlowChartGenerator()._create_dag(flow_instance)
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
            """graph TD;\n"""  # this will be passed to mermaid-js for rendering
        )
        # iterate through graph levels
        for level in graph.levels:
            # iterate through each node in the list of levels [node1, node2]
            for node in level:  # each node is an actual Node object
                for next_node in node.next:
                    # edge string represents a connection in mermaid js
                    edge_string = f"    {node.name}({node.name})==>{next_node}({next_node});\n"  # this will look create_data(create_data)==>transformation_function_2(transformation_function_2)
                    mermaid_js_string += edge_string

        return mermaid_js_string


    @classmethod
    def _create_descriptive_dag(cls, flow_instance) -> str:
        """This method is used to create a more descriptive graph from a Flow instance

        We use subgraphs to enclose a function and its accompanying description in them

        Args:
            flow_instance(BaseFlow): An instance of subclass of BaseFlow
            descriptive(bool): A bool value to add description to DAG display, defaults to True

        Returns:
            mermaid_js_string(str): A string value of mermaid js string
        """
        # base mermaid js string start
        graph = flow_instance.graph  # get the graph attribute which is Graph object
        mermaid_js_string = (
            """graph TD;\n"""  # this will be passed to mermaid-js for rendering
        )



        # we iterate over the graph levels
        for level in graph.levels:
            # iterate over each node in level
            for node in level:
                for next_node in node.next: # iterate over the next of the node
                    edge_subgraph = f"subgraph Step: {node.name.replace('_', '-')};\n" # subgraph name will be the node name replacing underscores with -
                    # node.name(node.name) += ~~~ node.docstring() or None
                    node_name_edge = f"   {node.name}({node.name})"
                    if node.docstring: # if docstring is present we create an invisible link with `~~~` notation
                        node_docstring_edge = f' ~~~ {node.name}_description[["""{node.docstring}"""]];\n'
                    else: #otherwise just skip to the next string
                        node_docstring_edge = ";\n"

                    end_subgraph = "end;\n\n" # end the subgraph
                    # add the next edge connection node.docstring() or node.name ==> next_node
                    if node.docstring: # if docstring is present then we assign that as the next connection
                        next_node_edge = f"{node.name}_description ==> {next_node};\n\n"
                    else: # otherwise the connection is direct from the node to the next
                        next_node_edge = f"{node.name} ==> {next_node};\n\n"


                    edge_string = edge_subgraph + node_name_edge + node_docstring_edge + end_subgraph + next_node_edge # put all the strings together

                    mermaid_js_string += edge_string



        return mermaid_js_string

    @classmethod
    def dag(cls, flow_instance, save_file: bool = False, path: str = None, description: bool= True) -> str:
        """Class method to generate DAG from Flow in the form of html output

        We use the Flow class to generate a flowchart and return the html content. This method can
        be used to save locally or use the html content elsewhere

        Args:
            flow_instance: An instance of BaseFlow subclass object
            save_file: Bool value to save file, defaults to False
            path: A path to save file
            description: Bool value of saving description of class

        Returns:
            content: The html data containing the flow diagram
        """
        if description:
            mermaid_js_string = cls._create_descriptive_dag(flow_instance=flow_instance)
        else:
            mermaid_js_string = cls._create_dag(flow_instance=flow_instance)

        root = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(root, "templates")
        environment = Environment(
            loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True
        )
        template = environment.get_template("base.html")

        flow_name = flow_instance.__class__.__name__  # Output eg.'ExamplePandas'

        # if path is provided, we use that also

        filename = f"{flow_name.lower()}.html"  # Output eg. examplepandas.html

        if path:  # path has a value
            os.makedirs(path, exist_ok=True) # create the directory if it does not exit
            filename = path + filename
            # if path has a value we can safely assume that they want to save to that path
            save_file = True  # we change the value to True to make sure we save i

        content = template.render(
            flow_name=flow_name, mermaid_js_string=mermaid_js_string
        )

        # if save_file is true we save the file in the local directory from where it is running
        if save_file:  # if save_file is true
            with open(filename, mode="w", encoding="utf-8") as message:
                logger.debug("Saving file: %s", filename)
                message.write(content)
                logger.debug("Saved file %s", filename)

        return content

    @classmethod
    def display(cls, flow_instance, description:bool =False) -> None:
        """Class method to display the DAG of the Flow

        This method only works in IPython style notebooks. Does not work in script
        This method displays the flowchart of the Flow based the Flow class itself.

        Args
            flow_instance: An instance of subclass of BaseFlow
            description: A bool value of descriptive, descriptive on adds docstring to DAG

        Returns:
            None: display the flowchart of the Flow
        """

        # get the flowchart mermaid js
        # in the form of eg. output:
        # """
        # graph LR;
        #   A--> B & C & D;
        # """"
        graph = cls._create_dag(flow_instance=flow_instance, description=description)
        graphbytes = graph.encode("ascii")
        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")
        display(Image(url="https://mermaid.ink/img/" + base64_string))
