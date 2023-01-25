"""Module for decorators"""
from typing import Callable
from functools import wraps


def step(function: Callable = None, next: str = None):
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
    func.is_step = True
    func.is_start = True
    func.name = func.__name__
    return func

def end(func: Callable) -> Callable:
    """This decorator indicates the end of a flow"""
    func.is_step = True
    func.is_end = True
    func.name = func.__name__
    return func




