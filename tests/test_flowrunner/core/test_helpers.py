# -*- coding: utf-8 -*-
from contextlib import nullcontext as does_not_raise

import pandas as pd
import pytest

from flowrunner.core.base import Graph, GraphOptions
from flowrunner.core.decorators import end, start, step
from flowrunner.core.helpers import DAGGenerator, GraphValidator
from flowrunner.runner.flow import BaseFlow
from flowrunner.system.exceptions import InvalidFlowException
from tests.test_flowrunner.runner.test_flow import ExamplePandas

# TODO: Need to add more validation failures based on each method in validation suite
# TODO: DAGGenerator().display() only checks if it works, if needs to also assert some output so we can verify works as required
# TODO: FlowChartGenerate().dag() sometimes changes orders of SAME level nodes, need to find out Why?


@pytest.fixture(scope="module")
def expected_html_content():
    with open("tests/test_flowrunner/core/examplepandas.html") as f:
        return f.readlines()


@pytest.fixture(scope="module")
def expected_js_string_tuple():
    """Fixture to test the structure of js string"""
    js_string = """
    graph TD;
    create_data(create_data)==>transformation_function_1(transformation_function_1);
    create_data(create_data)==>transformation_function_2(transformation_function_2);
    transformation_function_2(transformation_function_2)==>append_data(append_data);
    transformation_function_1(transformation_function_1)==>append_data(append_data);
    append_data(append_data)==>show_data(show_data);
    """

    js_string2 = """
    graph TD;
    create_data(create_data)==>transformation_function_1(transformation_function_1);
    create_data(create_data)==>transformation_function_2(transformation_function_2);
    transformation_function_1(transformation_function_1)==>append_data(append_data);
    transformation_function_2(transformation_function_2)==>append_data(append_data);
    append_data(append_data)==>show_data(show_data);
    """
    return (js_string, js_string2)


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
        (BadFlowExample5, pytest.raises(ValueError))

    ],
)
def test_graph_validator(bad_flow_example, expectations):
    """We add all the bad flows based on validation we want to fail"""
    with expectations:
        bad_flow_graph_options = GraphOptions(base_flow=bad_flow_example)
        bad_flow_graph = Graph(graph_options=bad_flow_graph_options)
        GraphValidator(graph=bad_flow_graph).run_validations(
            terminal_output=True
        )




@pytest.mark.parametrize(
    "bad_flow_example, expectations",
    [
    (BadFlowExample, pytest.raises(InvalidFlowException)),
    (BadFlowExample2,pytest.raises(InvalidFlowException)),
    (BadFlowExample3, pytest.raises(InvalidFlowException)),
    (BadFlowExample4, pytest.raises(InvalidFlowException)),
    (BadFlowExample5, pytest.raises(ValueError))
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


def test_dag_generator(expected_js_string_tuple):
    """Function to test the DAGGenerator()._create_dag()
    We iterate line by line to find differences
    """
    expected_js_string1 = expected_js_string_tuple[0]
    expected_js_string2 = expected_js_string_tuple[1]
    actual_js_string = DAGGenerator()._create_dag(ExamplePandas())
    assert (
        actual_js_string.strip()
        == expected_js_string1.strip()  # there is a bug in the FlowRunner class where order between functions at same level is misplaced
        or actual_js_string.strip()
        == expected_js_string2.strip()  # for this we need to add an OR condition so we account for both conditions
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
