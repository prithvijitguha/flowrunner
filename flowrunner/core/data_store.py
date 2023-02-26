"""Module for Data Store class"""
from dataclasses import dataclass, field
from typing import Dict

# Data Store will be a class which to handle all data passing between steps
# instance is always a plain dict
@dataclass
class DataStore:
    """Attributes
    data: A dict with key of function name and value of output
    """
    data: dict = field(default_factory=lambda: dict())




def read_output(function_name: str):
    """A function to read output from
    function"""
    pass






