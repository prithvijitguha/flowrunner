from dataclasses import dataclass
import click
from flowrunner.runner.flow import Graph
from flowrunner.system.exceptions import InvalidFlowException


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

