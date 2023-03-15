# -*- coding: utf-8 -*-
"""Module to generate html pages
This feature is NOT READY YET
"""

import os

from jinja2 import Environment, FileSystemLoader

from examples.pandas_example import ExamplePandas
from flowrunner.core.base import Graph, GraphOptions
from flowrunner.system.logger import logger

graph_options = GraphOptions(ExamplePandas)
graph = Graph(graph_options)

levels = graph.levels

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, "templates")
environment = Environment(
    loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True
)
template = environment.get_template("base_test.html")


filename = "test_final.html"
logger.debug("Saving file: %s", filename)
content = template.render(levels=levels)

print(content)
with open(filename, mode="w", encoding="utf-8") as message:
    message.write(content)
    logger.debug("Saved file %s", filename)
