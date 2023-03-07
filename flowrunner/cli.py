"""Module for cli commands"""
import click
import inspect
from flowrunner import BaseFlow
from pydoc import importfile


# @click.command()
# @click.argument("filepath")
# def hello(filepath):
#     click.echo(filepath)

# if __name__=="__main__":
#     hello()


def _read_python_file(file_path):
    """Function to read Python file from path"""
    module = importfile(file_path)
    #module = importfile(file_path)
    module_elements_dict = vars(module) # get module elements in dict eg. {'BaseFlow': <class 'flowrunner.runner.flow.BaseFlow'>, 'ExampleFlow': <class 'testing.ExampleFlow'>}
    # iterate over all and check if subclass of BaseFlow unless its __name__ is BaseFlow itself
    #flows = [] # a list to store all the subclass of BaseFlow
    flows = [element for element in module_elements_dict.values() if inspect.isclass(element) and issubclass(element, BaseFlow) and element.__name__ != BaseFlow.__name__]
    if len(flows) > 1:
        raise ValueError(f"Only 1 Flow are allowed per python file. Found {len(flows)}")
    return flows

_read_python_file(r"c:\Users\prith\Documents\VSCode_Workspace\Repos\flowrunner\testing.py")






