# -*- coding: utf-8 -*-
"""Module for cli commands
Usage: python -m flowrunner [OPTIONS] COMMAND [ARGS]...

  Welcome to FlowRunner! 🚀

  FlowRunner is a lightweight package to organize and represent Data
  Engineering/Science workflows. Its designed to be integrated with any pre-
  existing framework like pandas or PySpark

  Main FeaturesEasy BaseFlow to use to build Flows off ofSimple
  decorators to convert methods to Flow methodsCommand Line Interface for
  running Flows

Options:
  --help  Show this message and exit.

Commands:
  run       Command to run a Flow
  show      Command to show the order of iteration of a Flow
  validate  Command to validate a Flow


"""
import inspect
from pydoc import importfile

import click

from flowrunner import BaseFlow
from flowrunner.system.logger import logger


@click.group()
def cli():
    """Welcome to FlowRunner! 🚀

    FlowRunner is a lightweight package to organize and represent Data Engineering/Science workflows. Its designed to be
    integrated with any pre-existing framework like pandas or PySpark

    Main Features
    - Easy BaseFlow to use to build Flows off of
    - Simple decorators to convert methods to Flow methods
    - Command Line Interface for running Flows
    """
    pass


@cli.command()
@click.argument("filepath")
def validate(filepath: str):
    """Command to validate a Flow

    Examples:
        python -m flowrunner validate /my_path/to/flow_file.py

    Args:
        filepath: A string value of python file containing a Flow i.e subclass of BaseFlow

    Returns:
        Output regarding the validation of the flow
    """
    flow_list = _read_python_file(filepath)
    for flow_class in flow_list:
        logger.info("Validating flow %s", flow_class.__name__)
        flow_class().validate()


@cli.command()
@click.argument("filepath")
def show(filepath: str):
    """Command to show the order of iteration of a Flow

    Examples:
        python -m flowrunner show /my_path/to/flow_file.py

    Args:
        filepath: A string value of python file containing a Flow i.e subclass of BaseFlow

    Returns:
        Shows the order of iteration and explaination of Flow
    """
    flow_list = _read_python_file(filepath)
    for flow_class in flow_list:
        logger.info("Checking flow %s", flow_class.__name__)
        flow_class().show()


@cli.command()
@click.argument("filepath")
def run(filepath: str):
    """Command to run a Flow

    Examples:
        python -m flowrunner run /my_path/to/flow_file.py

    Args:
        filepath: A string value of python file containing a Flow i.e subclass of BaseFlow

    Returns:
        Runs the Flow
    """
    flow_list = _read_python_file(filepath)
    for flow_class in flow_list:
        logger.info("Running flow %s", flow_class.__name__)
        flow_class().run()


def _read_python_file(file_path: str) -> BaseFlow:
    """Function to read Python file from path
    An internal function that is used to read a file from a string value.

    Args:
        file_path: A string value of file path

    Returns:
        flows: A list value of all subclasses of BaseFlow except for BaseFlow itself
    """
    module = importfile(
        file_path
    )  # importfile is the best way to handle importing a module from a string
    module_elements_dict = vars(
        module
    )  # get module elements in dict eg. {'BaseFlow': <class 'flowrunner.runner.flow.BaseFlow'>, 'ExampleFlow': <class 'testing.ExampleFlow'>}
    # iterate over all and check if subclass of BaseFlow unless its __name__ is BaseFlow itself
    # flows = [] # a list to store all the subclass of BaseFlow
    flows = [
        element
        for element in module_elements_dict.values()
        if inspect.isclass(element)
        and issubclass(element, BaseFlow)
        and element.__name__ != BaseFlow.__name__
    ]
    flow_names = [flow.__name__ for flow in flows]
    logger.info("Found Flows: %s", flow_names)
    return flows


if __name__ == "__main__":
    cli()
