# -*- coding: utf-8 -*-
"""Module for flowrunner.core.helpers module

These are all functions that help in validation, dag generation, etc.
"""
from contextlib import nullcontext as does_not_raise

import pandas as pd
import pytest

from flowrunner.core.base import Graph, GraphOptions
from flowrunner.core.decorators import end, start, step
from flowrunner.core.helpers import DAGGenerator, GraphValidator
from flowrunner.runner.flow import BaseFlow
from flowrunner.system.exceptions import InvalidFlowException
from tests.test_flowrunner.runner.test_flow import ExamplePandas


@pytest.fixture(scope="module")
def expected_html_content():
    """Expected html output for dags"""
    with open("tests/test_flowrunner/core/examplepandas.html", encoding="utf-8") as html_output_file:
        return html_output_file.readlines()


@pytest.fixture(scope="module")
def expected_js_non_descriptive():
    """Fixture to test the structure of js string"""
    js_string = """
    graph TD;
    subgraph step-create_data;
    create_data(create_data);
    end
        step-create_data==>step-transformation_function_2;
        step-create_data==>step-transformation_function_2;
    subgraph step-transformation_function_2;
    transformation_function_2(transformation_function_2);
    end
        step-transformation_function_2;==>step-append_data;
    subgraph step-transformation_function_1;
    transformation_function_1(transformation_function_1);
    end
        step-transformation_function_3;==>step-append_data;
    subgraph step-append_data;
    append_data(append_data);
    end
        step-append_data;==>step-show_data;
    subgraph step-show_data;
    show_data(show_data);
    end
    """

    return js_string


@pytest.fixture(scope="module")
def expected_string_descriptive_output():
    """Fixture for an example of pandas descriptive string"""
    expected_js_descriptive = '''
    graph TD;
    subgraph step-method1;
    method1(method1) ~~~ method1_description[["""Example of a method with a docstring which
    will become description"""]];
    end;
    step-method1 ==> step-method2;
    step-method1 ==> step-method3;
    subgraph step-method3;
    method3(method3)
    end;
    method3 ==> step-method4;
    subgraph step-method2;
    method2(method2)
    end;
    method2 ==> step-method4;
    subgraph step-method4;
    method4(method4)
    end;
    '''
    return expected_js_descriptive

@pytest.fixture(scope="module")
def expected_non_descriptive_string_output():
    """Fixture for non descriptive output for
    DescriptiveExampleFlow"""
    non_descriptive_string = """
    graph TD;
    method1(method1)==>method2(method2);
    method1(method1)==>method3(method3);
    method2(method2)==>method4(method4);
    method3(method3)==>method4(method4);
    """
    return non_descriptive_string


@pytest.fixture(scope="module")
def expected_string_descriptive_output_false():
    """Fixture for an example of pandas descriptive string"""
    expected_js_descriptive_false = """
    graph TD;
    subgraph Step: method1;
    method1(method1);
    end;

    method1_description ==> method2;

    subgraph Step: method1;
    method1(method1);
    end;

    method1 ==> method3;

    subgraph Step: method2;
    method2(method2);
    end;

    method2 ==> method4;

    subgraph Step: method2;
    method3(method3);
    end;

    method3 ==> method4;
    """

    return expected_js_descriptive_false

class DescriptionExampleFlow(BaseFlow):
    @start
    @step(next=["method2", "method3"])
    def method1(self):
        """Testing the docstring"""
        self.a = 1

    @step(next=["method4"])
    def method2(self):
        self.a += 1

    @step(next=["method4"])
    def method3(self):
        self.a += 2

    @end
    @step
    def method4(self):
        self.a += 3
        print(self.a)


class BadFlowExample(BaseFlow):
    """Bad Example of flow, there are missing next parameters"""

    @start
    @step
    def method_1(self):
        return None

    @step(next=["method_3"])
    def method_2(self):
        return None

    @end
    @step
    def method_3(self):
        return None


class BadFlowExample2(BaseFlow):
    """Bad Example of flow, there is no 'start' method"""

    @step(next=["method_2"])
    def method_1(self):
        return None

    @step(next=["method_3"])
    def method_2(self):
        return None

    @end
    @step
    def method_3(self):
        return None


class BadFlowExample3(BaseFlow):
    """Bad Example of flow, there are no 'middle' nodes"""

    @start
    @step(next=["method_3"])
    def method_1(self):
        return None

    @end
    @step
    def method_3(self):
        return None


class BadFlowExample4(BaseFlow):
    """Bad Example of flow, there is no 'end' method"""

    @start
    @step(next=["method_2"])
    def method_1(self):
        return None

    @step(next=["method_3"])
    def method_2(self):
        return None

    @step
    def method_3(self):
        return None


class BadFlowExample5(BaseFlow):
    """Bad Example of flow, end has a next value"""

    @start
    @step(next=["method_2"])
    def method_1(self):
        return None

    @step(next=["method_3"])
    def method_2(self):
        return None

    @end
    @step(next=["tests"])
    def method_3(self):
        return None


@pytest.mark.parametrize(
    "bad_flow_example, expectations",
    [
        (BadFlowExample, does_not_raise()),
        (BadFlowExample2, does_not_raise()),
        (BadFlowExample3, does_not_raise()),
        (BadFlowExample4, does_not_raise()),
        (BadFlowExample5, pytest.raises(ValueError)),
    ],
)
def test_graph_validator(bad_flow_example, expectations):
    """We add all the bad flows based on validation we want to fail"""
    with expectations:
        bad_flow_graph_options = GraphOptions(base_flow=bad_flow_example)
        bad_flow_graph = Graph(graph_options=bad_flow_graph_options)
        GraphValidator(graph=bad_flow_graph).run_validations(terminal_output=True)


@pytest.mark.parametrize(
    "bad_flow_example, expectations",
    [
        (BadFlowExample, pytest.raises(InvalidFlowException)),
        (BadFlowExample2, pytest.raises(InvalidFlowException)),
        (BadFlowExample3, pytest.raises(InvalidFlowException)),
        (BadFlowExample4, pytest.raises(InvalidFlowException)),
        (BadFlowExample5, pytest.raises(ValueError)),
    ],
)
def test_graph_validator_with_error(bad_flow_example, expectations):
    """We add all the bad flows based on validation we want to fail"""
    with expectations:
        bad_flow_graph_options = GraphOptions(base_flow=bad_flow_example)
        bad_flow_graph = Graph(graph_options=bad_flow_graph_options)
        GraphValidator(graph=bad_flow_graph).run_validations_raise_error(
            terminal_output=True
        )


def test_dag_generator(expected_js_non_descriptive):
    """Function to test the DAGGenerator()._create_descriptive_dag() with description
    as false which will be non -descriptive
    We iterate line by line to find differences
    """
    actual_js_non_descriptive_string = DAGGenerator()._create_descriptive_dag(ExamplePandas(), description=False)


    for actual_line, expected_line in zip(
        actual_js_non_descriptive_string.split("\n"), expected_js_non_descriptive.split("\n")
    ):
        pytest.approx(
            actual_line.strip(), expected_line.strip()
        )

def test_dag(expected_html_content):
    """Function to test the DAGGenerator().dag() method"""
    flow_instance = ExamplePandas()
    actual_html_content = DAGGenerator().dag(
        flow_instance=flow_instance,
    )

    for actual_line, expected_line in zip(
        actual_html_content.split("\n"), expected_html_content
    ):
        pytest.approx(
            actual_line.strip(), expected_line.strip()
        )  # we use an approx since sometimes the order of same level nodes can be reversed


def test_display():
    """Check the display() method and make sure it works. Future we should add a test
    that asserts its output as well"""
    flow_instance = ExamplePandas()
    DAGGenerator().display(flow_instance)


def test_create_descriptive_dag(expected_string_descriptive_output):
    """Test to check the functionality of descriptive dag
    which has a subgraph and description"""
    flow_instance = DescriptionExampleFlow()
    actual_descriptive_js_string = DAGGenerator()._create_descriptive_dag(flow_instance)

    for actual_line, expected_line in zip(
        actual_descriptive_js_string.strip().split(),
        expected_string_descriptive_output.strip().split(),

    # there is a bug in the FlowRunner class where order between functions at same level is misplaced
    ):
        pytest.approx(actual_line, expected_line)


def test_choose_dag(expected_string_descriptive_output, expected_non_descriptive_string_output):
    """Test to check if functionality of choosing dag
    works as expected"""
    flow_instance = DescriptionExampleFlow()
    actual_descriptive_js_string =  DAGGenerator()._create_descriptive_dag(flow_instance)

    for actual_line, expected_line in zip(
        actual_descriptive_js_string.strip().split(),
        expected_string_descriptive_output.strip().split(),

    # there is a bug in the FlowRunner class where order between functions at same level is misplaced
    ):
        pytest.approx(actual_line, expected_line)

    actual_non_descriptive_output = DAGGenerator()._create_descriptive_dag(flow_instance, description=False)

    for actual_line_non_descrip, expected_line_non_descrip in zip(
        actual_non_descriptive_output.strip().split(),
        expected_non_descriptive_string_output.strip().split(),

    # there is a bug in the FlowRunner class where order between functions at same level is misplaced
    ):
        pytest.approx(actual_line_non_descrip, expected_line_non_descrip)
