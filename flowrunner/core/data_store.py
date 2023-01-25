"""Module for Data Store class"""
from dataclasses import dataclass, field
from typing import Dict

# Data Store will be a class which to handle all data passing between steps
# instance is always a plain dict
@dataclass
class DataStore:
    """Attributes
    data_store: A dict
    """
    data_store: Dict = field(default_factory=lambda: {})
    # get value from data_store
    def read_data(self, key):
        return self.data_store[key]

    # set value from data_store
    def store_data(self, key, value):
        self.data_store[key] = value





