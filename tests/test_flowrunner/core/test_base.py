from flowrunner.core.decorators import step, start, end
from flowrunner.runner.flow import Node


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

