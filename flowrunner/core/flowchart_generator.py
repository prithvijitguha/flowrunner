# -*- coding: utf-8 -*-
"""Module to generate html pages
This feature is NOT READY YET
"""

import os

import flow_example
from jinja2 import Environment, FileSystemLoader
from runner import FlowRunner
from system.logger import logger

flow = FlowRunner(flow_example)
flow.validate()
flow._traverse_graph()


root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, "templates")
environment = Environment(loader=FileSystemLoader(templates_dir))
template = environment.get_template("base.html")


filename = f"flowchart_{flow_example.__name__}.html"
logger.debug("Saving file: %s", filename)
content = template.render(
    nodes=flow.nodes, edges=flow.edges, flow_name=flow_example.__name__
)
with open(filename, mode="w", encoding="utf-8") as message:
    message.write(content)
    logger.debug("Saved file %s", filename)
