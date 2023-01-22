import flow_example
import click
from dataclasses import dataclass, field
from networkx import DiGraph
from inspect import getmembers
from typing import Any

@dataclass
class FlowRunner:
    """FlowRunner is a class to run all steps in a flow"""
    module: Any
    graph: DiGraph = field(default_factory=lambda: DiGraph())
    def __post_init__(self):
        self.functions = {name: [value, value.next] for name, value in self.module.__dict__.items() if callable(value) and hasattr(value, 'is_step')}


    def validate(self):
        # iterate over functions
        for key, value in self.functions.items():
            next = value[1]
            # check if they are all 'steps'
            # check if their next is in the dir()
            if next not in dir(self.module):
                click.secho(f"Node {next} not in graph")


    def _traverse_graph(self):
        for name, value in self.module.__dict__.items():
            if callable(value) and hasattr(value, 'is_step'):
                click.secho(value.name, fg='green')
                click.secho(value.__doc__, fg='bright_red')
                click.secho(f"Next Callable: {value.next}", fg='blue')
                click.echo("\n")


flow = FlowRunner(flow_example)
flow.validate()
flow._traverse_graph()





