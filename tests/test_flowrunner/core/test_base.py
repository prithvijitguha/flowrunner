from flowrunner.core.base  import Node, GraphOptions, Graph
from flowrunner.runner.flow import BaseFlow, FlowRunner
from flowrunner.core.decorators import step, start, end
import pytest

class TestNode:
    """Class to test Node class and decorators"""
    @pytest.fixture(scope="module")
    def example_node_flow(self):
        """Method to return example flow"""
        class ExampleNodeFlow(BaseFlow):
            @start
            @step(next=["method_2", "method_3"])
            def method_1(self):
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

    def test_node_start(self, example_node_flow):
        """Function to test start nodes"""
        assert example_node_flow.method_1.is_step == True
        assert example_node_flow.method_1.is_start == True
        assert example_node_flow.method_1.next == ["method_2", "method_3"]
        assert hasattr(example_node_flow.method_3, "end") == False


    def test_node_middle(self, example_node_flow):
        """Function to test start nodes"""
        assert example_node_flow.method_2.is_step == True
        assert example_node_flow.method_3.is_step == True
        assert example_node_flow.method_2.next == ["method_4"]
        assert example_node_flow.method_3.next == ["method_4"]
        assert hasattr(example_node_flow.method_3, "end") == False
        assert hasattr(example_node_flow.method_3, "start") == False


    def test_node_end(self, example_node_flow):
        """Function to test start nodes"""
        assert example_node_flow.method_4.is_end == True
        assert example_node_flow.method_4.is_end == True
        assert example_node_flow.method_4.next == None
        assert hasattr(example_node_flow.method_3, "start") == False












# def test_node():
#     """Function to test whether Node works
#     as expected"""
#     node_example = Node(test_example_callable.__name__, test_example_callable)

#     assert node_example.name == 'test_example_callable'
#     assert node_example.function_reference == test_example_callable


# def test_graph_options():
#     graph_options = GraphOptions(base_flow=FlowExample)
#     assert len(graph_options.start) == 1
#     assert len(graph_options.middle_nodes) == 3
#     assert len(graph_options.end) == 1
#     assert graph_options.start[0].name == FlowExample.first_func.__name__
#     assert graph_options.middle_nodes[0].name == FlowExample.middle_func.__name__
#     assert graph_options.middle_nodes[1].name == FlowExample.another_middle_func.__name__
#     assert graph_options.middle_nodes[2].name == FlowExample.model_func.__name__
#     assert graph_options.end[0].name == FlowExample.end_func.__name__


# def test_graph():
#     graph_options = GraphOptions(base_flow=FlowExample)
#     graph = Graph(graph_options)
#     graph_levels = graph.levels
#     assert len(graph_levels[0]) == 1 # the first level/root marked with @start
#     assert len(graph_levels[1]) == 2 # the next set of methods next of the root
#     assert len(graph_levels[2]) == 1 # the next set of functions mentioned
#     assert len(graph_levels[3]) == 1 # the last level marked with @eb
#     assert len(graph_levels) == 4





