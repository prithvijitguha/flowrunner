# -*- coding: utf-8 -*-
from flowrunner import BaseFlow, end, start, step
from flowrunner.core.helpers import DAGGenerator


class ExampleFlow(BaseFlow):
    @start
    @step(next=["method2", "method3"])
    def method1(self):
        """Testing the docstring"""
        self.a = 1

    @step(next=["method4"])
    def method2(self):
        self.a += 1

    @step(next=["method4"])
    def method3(self):
        self.a += 2

    @end
    @step
    def method4(self):
        self.a += 3
        print(self.a)


example_flow = ExampleFlow()

graph = DAGGenerator()._create_descriptive_dag(example_flow)

print(graph)
