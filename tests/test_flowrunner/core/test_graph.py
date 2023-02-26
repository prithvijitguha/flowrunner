from flowrunner.core.graph import Node, GraphOptions
from flowrunner.decorators import step, start, end


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


def test_node():
    """Function to test whether Node works
    as expected"""
    node_example = Node(test_example_callable.__name__, test_example_callable)

    assert node_example.name == 'test_example_callable'
    assert node_example.function_reference == test_example_callable


def test_graph_options():
    graph_options = GraphOptions(module=[
        test_example_callable,
        test_example_callable_2,
        test_example_callable_3,
        test_example_callable_4
    ])

    assert len(graph_options.start) == 1
    assert len(graph_options.middle_nodes) == 2
    assert len(graph_options.end) == 1
    assert graph_options.start[0].name == test_example_callable.__name__
    assert graph_options.middle_nodes[0].name == test_example_callable_2.__name__
    assert graph_options.middle_nodes[1].name == test_example_callable_3.__name__
    assert graph_options.end[0].name == test_example_callable_4.__name__



