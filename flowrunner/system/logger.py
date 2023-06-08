# -*- coding: utf-8 -*-
"""
Module for logging
"""
import logging

import coloredlogs  # pylint: disable=import-error

LOG_FORMAT='%(levelname)s | %(message)s | %(asctime)s | %(hostname)s | %(name)s | %(process)d '

# Create a logger object.
logger = logging.getLogger(__name__)
# By default the install() function installs a handler on the root logger,
# this means that log messages from your code and log messages from the
# libraries that you use will all show up on the terminal.
# eg. coloredlogs.install(level="DEBUG")

# If you don't want to see log messages from libraries, you can pass a
# specific logger object to the install() function. In this case only log
# messages originating from that logger will show up on the terminal.

coloredlogs.install(fmt=LOG_FORMAT, level="DEBUG", logger=logger)

# suppress the py4j logger if its there
py4jlogger = logging.getLogger("py4j")
py4jlogger.setLevel(logging.INFO)
