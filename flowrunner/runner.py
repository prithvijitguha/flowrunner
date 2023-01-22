import flow_example
import click
from dataclasses import dataclass, field
from networkx import DiGraph
from inspect import getmembers
from typing import Any

@dataclass
class FlowRunner:
    module: Any
    graph: DiGraph = field(default_factory=lambda: DiGraph())
    def __post_init__(self):
        self.functions = {name: value for name, value in self.module.__dict__.items() if callable(value) and hasattr(value, 'is_step')}
        self.nodes = [(key, value.next) for key, value in self.functions.items()]

    def validate(self):
        # iterate over functions and check
        for func_next_tuple in self.nodes:
            temp_func = func_next_tuple[0]
            temp_next = func_next_tuple[1]
            if temp_next not in dir(self.module):
                click.secho(f"{temp_next} not in module", fg="red")
            if not hasattr(temp_next, 'is_step'):
                click.secho(f"{temp_next} not 'step' ", fg="red")

        # if func is module and func is_step




    def _traverse_graph(self):
        for name, value in self.module.__dict__.items():
            if callable(value) and hasattr(value, 'is_step'):
                click.secho(value.name, fg='green')
                click.secho(value.__doc__, fg='bright_red')
                click.secho(f"Next Callable: {value.next}", fg='blue')
                click.echo("\n")


flow = FlowRunner(flow_example)
#flow.validate()
flow._traverse_graph()





