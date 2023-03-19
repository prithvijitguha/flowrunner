# -*- coding: utf-8 -*-
from contextlib import nullcontext as does_not_raise

import pytest

from flowrunner.core.base import Graph, GraphOptions
from flowrunner.core.decorators import end, start, step
from flowrunner.runner.flow import BaseFlow


class ExampleNodeFlow(BaseFlow):
    @start
    @step(next=["method_2", "method_3"])
    def method_1(self):
        """Test Docstring sample"""
        return None

    @step(next="method_4")
    def method_2(self):
        return None

    @step(next=["method_4"])
    def method_3(self):
        return None

    def example_method(self):
        """This method is there to make
        sure that our GraphOptions are being filtered correctly for
        @step, @end and @start methods"""
        return None

    @end
    @step
    def method_4(self):
        return None


class ExampleNodeFlow2(BaseFlow):
    @start
    @step(next=["method_3"])
    def method_1(self):
        """Test Docstring sample"""
        return None

    @start
    @step(next=["method_3"])
    def method_2(self):
        return None

    @step(next=["method_4"])
    def method_3(self):
        return None

    @end
    @step
    def method_4(self):
        return None


@pytest.fixture(scope="session")
def example_node_flow():
    """Method to return example flow"""
    return ExampleNodeFlow


@pytest.fixture(scope="session")
def example_node_flow_2():
    """Method to return example flow"""
    return ExampleNodeFlow2


class TestNodeGraphGraphOptions:
    """Class to test Node class and decorators"""

    @pytest.fixture(scope="module")
    def example_graph_options(self, example_node_flow):
        graph_options = GraphOptions(example_node_flow)
        return graph_options

    @pytest.fixture(scope="module")
    def example_graph_options_2(self, example_node_flow_2):
        graph_options = GraphOptions(example_node_flow_2)
        return graph_options

    @pytest.fixture(scope="module")
    def example_graph(self, example_graph_options):
        graph = Graph(graph_options=example_graph_options)
        return graph

    @pytest.fixture(scope="module")
    def example_graph_2(self, example_graph_options_2):
        graph = Graph(graph_options=example_graph_options_2)
        return graph

    def test_graph_options(self, example_node_flow, example_graph_options):
        assert len(example_graph_options.start) == 1
        assert len(example_graph_options.middle_nodes) == 2
        assert len(example_graph_options.end) == 1
        assert (
            example_graph_options.start[0].name == example_node_flow.method_1.__name__
        )
        assert (
            example_graph_options.middle_nodes[0].name
            == example_node_flow.method_2.__name__
        )
        assert (
            example_graph_options.middle_nodes[1].name
            == example_node_flow.method_3.__name__
        )
        assert example_graph_options.end[0].name == example_node_flow.method_4.__name__

    def test_node(self, example_graph_options, example_node_flow):
        start_node = example_graph_options.start[0]
        assert start_node.name == "method_1"
        assert start_node.function_reference == example_node_flow.method_1
        assert start_node.next == ["method_2", "method_3"]
        assert start_node.docstring == example_node_flow.method_1.__doc__

    def test_graph(self, example_graph):
        graph_levels = example_graph.levels
        assert len(graph_levels[0]) == 1  # the first level/root marked with @start
        assert len(graph_levels[1]) == 2  # the next set of methods next of the root
        assert len(graph_levels[2]) == 1  # the next set of functions mentioned
        assert len(graph_levels) == 3

    def test_repr_string(self, example_graph_options):
        """Method to check the graph options string representation"""
        assert (
            str(example_graph_options)
            == "Start=[method_1]\nMiddle Nodes=[method_2, method_3]\nEnd=[method_4]"
        )

    def test_graph_options_2(self, example_node_flow_2, example_graph_options_2):
        assert len(example_graph_options_2.start) == 2
        assert len(example_graph_options_2.middle_nodes) == 1
        assert len(example_graph_options_2.end) == 1
        assert (
            example_graph_options_2.start[0].name
            == example_node_flow_2.method_1.__name__
        )
        assert (
            example_graph_options_2.start[1].name
            == example_node_flow_2.method_2.__name__
        )
        assert (
            example_graph_options_2.middle_nodes[0].name
            == example_node_flow_2.method_3.__name__
        )
        assert (
            example_graph_options_2.end[0].name == example_node_flow_2.method_4.__name__
        )

    def test_node_2(self, example_graph_2, example_node_flow_2):
        start_node = example_graph_2.start[0]
        assert start_node.name == "method_1"
        assert start_node.function_reference == example_node_flow_2.method_1
        assert start_node.next == ["method_3"]
        assert start_node.docstring == example_node_flow_2.method_1.__doc__

    def test_graph_2(self, example_graph_2):
        graph_levels = example_graph_2.levels
        assert len(graph_levels[0]) == 2  # the first level/root marked with @start
        assert len(graph_levels[1]) == 1  # the next set of methods next of the root
        assert len(graph_levels[2]) == 1  # the next set of functions mentioned
        assert len(graph_levels) == 3


class ExampleBadFlow(BaseFlow):
    """Example of Bad Flow, the next has different type of values
    in `method_2`"""

    @start
    @step(next=["bad_method_2", "bad_method_3"])
    def bad_method_1(self):
        """Test Docstring sample"""
        return None

    @step(next=["bad_method_4", 4])
    def bad_method_2(self):
        return None

    @step(next=["bad_method_4"])
    def bad_method_3(self):
        return None

    @end
    @step
    def bad_method_4(self):
        return None


class ExampleBadFlow2(BaseFlow):
    """Example of Bad Flow, the next has a dict value
    as `next` in `bad_method_2`"""

    @start
    @step(next=["bad_method_2", "bad_method_3"])
    def bad_method_1(self):
        """Test Docstring sample"""
        return None

    @step(next=("bad_method_4"))
    def bad_method_2(self):
        return None

    @step(next={"bad_method_4": "test"})
    def bad_method_3(self):
        return None

    @end
    @step
    def bad_method_4(self):
        return None


class ExampleBadFlow3(BaseFlow):
    """Example of Bad Flow, the next has duplicate values in
    method `bad_method2

    as `next` in `bad_method_2`"""

    @start
    @step(next=["bad_method_2", "bad_method_3"])
    def bad_method_1(self):
        """Test Docstring sample"""
        return None

    @step(next=["bad_method_4", "bad_method_4"])
    def bad_method_2(self):
        return None

    @step(next=["bad_method_4"])
    def bad_method_3(self):
        return None

    @end
    @step
    def bad_method_4(self):
        return None


class ExampleBadFlow4(BaseFlow):
    """Example of Bad Flow, the value of next is the current
    node name

    as `next` in `bad_method_2`"""

    @start
    @step(next=["bad_method_2", "bad_method_3"])
    def bad_method_1(self):
        """Test Docstring sample"""
        return None

    @step(next=["bad_method_2", "bad_method_4"])
    def bad_method_2(self):
        return None

    @step(next=["bad_method_4"])
    def bad_method_3(self):
        return None

    @end
    @step
    def bad_method_4(self):
        return None


class ExampleBadFlow5(BaseFlow):
    """Example of Bad Flow, `bad_method_4` has
    start, end and step decorator
    """

    @start
    @step(next=["bad_method_2", "bad_method_3"])
    def bad_method_1(self):
        """Test Docstring sample"""
        return None

    @step(next=["bad_method_4"])
    def bad_method_2(self):
        return None

    @step(next=["bad_method_4"])
    def bad_method_3(self):
        return None

    @end
    @start
    @step
    def bad_method_4(self):
        return None


class ExampleBadFlow6(BaseFlow):
    """Example of stranded node, not linked, but added as a step"""

    @start
    @step(next=["bad_method_2", "bad_method_3"])
    def bad_method_1(self):
        """Test Docstring sample"""
        return None

    @step(next=["bad_method_4"])
    def bad_method_2(self):
        return None

    @step(next=["bad_method_4"])
    def bad_method_3(self):
        return None

    @step
    def stranded_node(self):
        return None

    @end
    @step
    def bad_method_4(self):
        return None


@pytest.mark.parametrize(
    "flow, expectation",
    [
        (ExampleBadFlow, pytest.raises(TypeError)),
        (ExampleBadFlow2, pytest.raises(TypeError)),
        (ExampleBadFlow3, pytest.raises(ValueError)),
        (ExampleBadFlow4, pytest.raises(ValueError)),
        (ExampleBadFlow5, pytest.raises(ValueError)),
        (ExampleBadFlow6, does_not_raise()),
        (ExampleNodeFlow, does_not_raise()),
        (ExampleNodeFlow2, does_not_raise()),
    ],
)
def test_bad_flows_node_errors(flow, expectation):
    """Test to make sure we pick up errors that can break a
    GraphOptions and Graph.arrange_graph at Node level
    """
    with expectation:
        graph_options = GraphOptions(base_flow=flow)
        print(graph_options)
        graph = Graph(graph_options=graph_options)
