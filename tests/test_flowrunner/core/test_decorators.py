# -*- coding: utf-8 -*-
import pytest

from flowrunner.core.decorators import Step
from flowrunner.runner.flow import BaseFlow
from tests.test_flowrunner.core.test_base import example_node_flow


class TestDecorators:
    """Class to test decorators"""

    def test_node_start(self, example_node_flow):
        """Function to test start nodes, make sure
        that attributes are being correctly"""
        assert example_node_flow.method_1.is_step == True
        assert example_node_flow.method_1.is_start == True
        assert example_node_flow.method_1.next == ["method_2", "method_3"]
        assert hasattr(example_node_flow.method_3, "end") == False

    def test_node_middle(self, example_node_flow):
        """Function to test middle nodes, make sure
        that attributes are being correctly"""
        assert example_node_flow.method_2.is_step == True
        assert example_node_flow.method_3.is_step == True
        assert example_node_flow.method_2.next == "method_4"
        assert example_node_flow.method_3.next == ["method_4"]
        assert hasattr(example_node_flow.method_3, "end") == False
        assert hasattr(example_node_flow.method_3, "start") == False

    def test_node_end(self, example_node_flow):
        """Function to test end nodes, make sure
        that attributes are being correctly"""
        assert example_node_flow.method_4.is_end == True
        assert example_node_flow.method_4.is_end == True
        assert example_node_flow.method_4.next == None
        assert hasattr(example_node_flow.method_3, "start") == False

    @pytest.fixture(scope="module")
    def example_decorator_new_step_class(self):
        """Fixture to return function decorated with 'Step' class"""

        @Step
        def test_method():
            return None

        return test_method

    def test_step_class(self, example_decorator_new_step_class):
        """Test to check the new 'Step' class"""
        assert example_decorator_new_step_class.is_step == True
