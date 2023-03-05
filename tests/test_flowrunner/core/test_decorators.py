from flowrunner.core.decorators import step, start, end, Step
from flowrunner.runner.flow import BaseFlow
import pytest

class TestDecorators:
    """Class to test decorators"""
    @pytest.fixture(scope="module")
    def example_decorator_flow(self):
        """Method to return example flow"""
        class ExampleDecoratorFlow(BaseFlow):
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

        return ExampleDecoratorFlow

    def test_node_start(self, example_decorator_flow):
        """Function to test start nodes"""
        assert example_decorator_flow.method_1.is_step == True
        assert example_decorator_flow.method_1.is_start == True
        assert example_decorator_flow.method_1.next == ["method_2", "method_3"]
        assert hasattr(example_decorator_flow.method_3, "end") == False


    def test_node_middle(self, example_decorator_flow):
        """Function to test start nodes"""
        assert example_decorator_flow.method_2.is_step == True
        assert example_decorator_flow.method_3.is_step == True
        assert example_decorator_flow.method_2.next == ["method_4"]
        assert example_decorator_flow.method_3.next == ["method_4"]
        assert hasattr(example_decorator_flow.method_3, "end") == False
        assert hasattr(example_decorator_flow.method_3, "start") == False


    def test_node_end(self, example_decorator_flow):
        """Function to test start nodes"""
        assert example_decorator_flow.method_4.is_end == True
        assert example_decorator_flow.method_4.is_end == True
        assert example_decorator_flow.method_4.next == None
        assert hasattr(example_decorator_flow.method_3, "start") == False


    @pytest.fixture(scope="module")
    def example_decorator_new_step_class(self):
        """Fixture to 'Step' class"""
        @Step
        def test_method(self):
            return None

        return test_method

    def test_step_class(self, example_decorator_new_step_class):
        """Test to check the new 'Step' class"""
        assert example_decorator_new_step_class.is_step == True
