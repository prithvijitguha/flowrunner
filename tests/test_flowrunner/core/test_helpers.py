# -*- coding: utf-8 -*-
import pytest

from flowrunner.core.base import Graph, GraphOptions
from flowrunner.core.decorators import end, start, step
from flowrunner.core.helpers import GraphValidator
from flowrunner.runner.flow import BaseFlow
from flowrunner.system.exceptions import InvalidFlowException
from tests.test_flowrunner.runner.test_flow import ExamplePandas

# TODO: Need to add more validation failures based on each method in validation suite


@pytest.fixture(scope="module")
def expected_html_data():
    """Fixture for how the html final data should look"""
    with open("tests/test_flowrunner/core/examplepandas.html") as html_file:
        html_data = html_file.readlines()

    return html_data


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


def test_flowchart_generator(expected_html_data):
    """Function to test the flowchart_generator
    We iterate line by line to find differences
    """
    ExamplePandas().generate_html(True)

    with open("./examplepandas.html") as html_file:
        actual_html_data = html_file.readlines()
    # iterate line by line in the html data to check whether they
    # are equal
    for actual_html_line, expected_html_line in zip(
        actual_html_data, expected_html_data
    ):
        assert actual_html_line == expected_html_line
