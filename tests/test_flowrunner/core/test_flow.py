from flowrunner.core.flow import Node, GraphOptions, BaseFlow, GraphValidator, Graph
from flowrunner.core.decorators import step, start, end
import pytest

@start
@step
def test_example_callable():
    print("Hello World")

@step
def test_example_callable_2():
    print("Hello World")

@step
def test_example_callable_3():
    print("Hello World")

@end
@step
def test_example_callable_4():
    print("Hello World")



class FlowExample(BaseFlow):
    @start
    @step(next=['middle_func', 'another_middle_func'])
    def first_func(self):
        """This function is the start of our workflow
        where we extract 3 dataframes"""
        x = 2
        self.data_store['first_func'] = x
        print("first_func output", x)

    @step(next='model_func')
    def middle_func(self):
        """This function is the middle where we
        filter + transform stuff"""
        value_from_first = self.data_store['first_func']
        self.data_store['middle_func'] = value_from_first * 3
        print("middle_func output", self.data_store['middle_func'])



    @step(next='model_func')
    def another_middle_func(self):
        """This function is the middle where we
        filter + transform stuff"""

        value_from_first = self.data_store['first_func']
        self.data_store['another_middle_func'] = value_from_first
        print("another_middle_func output", value_from_first)

    @step(next='end_func')
    def model_func(self):
        """This function does model training"""
        y = self.data_store['middle_func']
        x = self.data_store['another_middle_func']
        self.data_store['model_func'] = x + y
        print("model_func output", x)
        print("model_func output", y)



    @end
    @step
    def end_func(self):
        """This function is the end where
        we write data into a table"""
        final_value = self.data_store['model_func']
        print("end_func output", final_value)





def test_node():
    """Function to test whether Node works
    as expected"""
    node_example = Node(test_example_callable.__name__, test_example_callable)

    assert node_example.name == 'test_example_callable'
    assert node_example.function_reference == test_example_callable


def test_graph_options():
    graph_options = GraphOptions(base_flow=FlowExample)
    assert len(graph_options.start) == 1
    assert len(graph_options.middle_nodes) == 3
    assert len(graph_options.end) == 1
    assert graph_options.start[0].name == FlowExample.first_func.__name__
    assert graph_options.middle_nodes[0].name == FlowExample.middle_func.__name__
    assert graph_options.middle_nodes[1].name == FlowExample.another_middle_func.__name__
    assert graph_options.middle_nodes[2].name == FlowExample.model_func.__name__
    assert graph_options.end[0].name == FlowExample.end_func.__name__


def test_graph():
    graph_options = GraphOptions(base_flow=FlowExample)
    graph = Graph(graph_options)
    graph_levels = graph.levels
    assert len(graph_levels[0]) == 1 # the first level/root marked with @start
    assert len(graph_levels[1]) == 2 # the next set of methods next of the root
    assert len(graph_levels[2]) == 1 # the next set of functions mentioned
    assert len(graph_levels[3]) == 1 # the last level marked with @eb
    assert len(graph_levels) == 4



def test_graph_validator():
    #graph_validtor = GraphValidator(base)
    pass




