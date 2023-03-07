# -*- coding: utf-8 -*-
"""Module for decorators"""
from functools import update_wrapper, wraps
from typing import Callable, List, Union


def step(function: Callable = None, next: Union[List, str] = None):
    """This decorator indicates a step in the function
    We add a 3 attributes to it is_step, name, next"""

    def _step(f):
        f.is_step = True
        f.name = f.__name__
        f.next = next

        @wraps(f)
        def wrapper(*args, **kwargs):
            # Do stuff with args here...
            return f(*args, **kwargs)

        return wrapper

    if function:
        return _step(function)
    return _step


def start(func: Callable) -> Callable:
    """This decorator indicates the start of a flow"""
    func.is_start = True
    func.name = func.__name__
    return func


def end(func: Callable) -> Callable:
    """This decorator indicates the end of a flow"""
    func.is_end = True
    func.name = func.__name__
    return func


class Step:
    """Step is a decorator class to convert
    any function to a 'step' function
    and have a next
    """

    def __init__(self, func: Callable, next: Union[str, list, None] = None):
        func.is_step = True
        func.next = next
        func.name = func.__name__
        self.func = func
        update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
