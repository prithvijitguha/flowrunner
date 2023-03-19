# -*- coding: utf-8 -*-
import pytest

from flowrunner.core.base import Graph, GraphOptions, Node
from flowrunner.core.decorators import end, start, step
from flowrunner.runner.flow import BaseFlow, FlowRunner


@pytest.fixture(scope="session")
def example_node_flow():
    """Method to return example flow"""

    class ExampleNodeFlow(BaseFlow):
        @start
        @step(next=["method_2", "method_3"])
        def method_1(self):
            """Test Docstring sample"""
            return None

        @step(next=["method_4"])
        def method_2(self):
            return None

        @step(next=["method_4"])
        def method_3(self):
            return None

        @end
        @step
        def method_4(self):
            return None

    return ExampleNodeFlow


class TestNodeGraphGraphOptions:
    """Class to test Node class and decorators"""

    @pytest.fixture(scope="module")
    def example_graph_options(self, example_node_flow):
        graph_options = GraphOptions(example_node_flow)
        return graph_options

    @pytest.fixture(scope="module")
    def example_graph(self, example_graph_options):
        graph = Graph(graph_options=example_graph_options)
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
        assert str(example_graph_options) == "Start=[method_1]\nMiddle Nodes=[method_2, method_3]\nEnd=[method_4]"


@pytest.fixture(scope="session")
def example_node_flow_2():
    """Method to return example flow"""

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

    return ExampleNodeFlow2


class TestNodeGraphGraphOptions2:
    """Class to test Node class and decorators"""

    @pytest.fixture(scope="module")
    def example_graph_options_2(self, example_node_flow_2):
        graph_options = GraphOptions(example_node_flow_2)
        return graph_options

    @pytest.fixture(scope="module")
    def example_graph_2(self, example_graph_options_2):
        graph = Graph(graph_options=example_graph_options_2)
        return graph

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
