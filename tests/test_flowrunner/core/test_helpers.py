from flowrunner.core.helpers import GraphValidator
from flowrunner.core.base import Graph, GraphOptions
from flowrunner.system.exceptions import InvalidFlowException
from flowrunner.runner.flow import BaseFlow
from flowrunner.core.decorators import step, start, end
import pytest

# TODO: Need to add more validation failures based on each method in validation suite


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
