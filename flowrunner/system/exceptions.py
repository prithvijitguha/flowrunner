# -*- coding: utf-8 -*-
"""Module to store any custom
exceptions
"""


class InvalidFlowException(Exception):
    """Exception when there is an Invalid flow detected"""

    pass


class CyclicFlowException(Exception):
    """Exception when there is a Cyclic flow detected"""

    pass
