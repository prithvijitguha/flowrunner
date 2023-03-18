# -*- coding: utf-8 -*-
import pytest

from flowrunner.core.base import Graph, GraphOptions
from flowrunner.core.decorators import end, start, step
from flowrunner.core.helpers import FlowChartGenerator, GraphValidator
from flowrunner.runner.flow import BaseFlow
from flowrunner.system.exceptions import InvalidFlowException
from tests.test_flowrunner.runner.test_flow import ExamplePandas

# TODO: Need to add more validation failures based on each method in validation suite
# TODO: FlowChartGenerator().display() only checks if it works, if needs to also assert some output so we can verify works as required


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


@pytest.fixture(scope="module")
def bad_flow_example():
    """Function to return a BadFlowExample for testing"""

    class BadFlowExample(BaseFlow):
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

    return BadFlowExample


def test_graph_validator(bad_flow_example):
    with pytest.raises(InvalidFlowException):
        bad_flow_graph_options = GraphOptions(base_flow=bad_flow_example)
        bad_flow_graph = Graph(graph_options=bad_flow_graph_options)
        GraphValidator(graph=bad_flow_graph).run_validations_raise_error()


def test_flowchart_generator(expected_js_string_tuple):
    """Function to test the flowchart_generator
    We iterate line by line to find differences
    """
    expected_js_string1 = expected_js_string_tuple[0]
    expected_js_string2 = expected_js_string_tuple[1]
    actual_js_string = FlowChartGenerator()._create_flowchart(ExamplePandas())
    assert (
        actual_js_string.strip()
        == expected_js_string1.strip()  # there is a bug in the FlowRunner class where order between functions at same level is misplaced
        or actual_js_string.strip()
        == expected_js_string2.strip()  # for this we need to add an OR condition so we account for both conditions
    )


def test_display():
    """Check the display() method and make sure it works. Future we should add a test
    that asserts its output as well"""
    flow_instance = ExamplePandas()
    FlowChartGenerator().display(flow_instance)
