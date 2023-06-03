# -*- coding: utf-8 -*-
"""
Module for logging
"""
import logging
from colorama import Fore, Style


LOG_FORMAT='%(levelname)s | %(message)s | %(asctime)s | %(name)s | %(process)d '

class ColoredOuputFormatter(logging.Formatter):
    # color schemes
    debug_color = Fore.BLUE
    info_color = Fore.GREEN
    warning_color = Fore.YELLOW
    error_color = Fore.MAGENTA
    critical_color = Fore.RED
    format = LOG_FORMAT

    # emoji schemes
    debug_emoji = "🐛"
    info_emoji = "📝"
    warning_emoji = "🦺"
    error_emoji = "🚨"
    critical_emoji = "💥"


    FORMATS = {
        logging.DEBUG: f"{debug_emoji} {Style.BRIGHT} {debug_color} {format}",
        logging.INFO: f"{info_emoji} {Style.BRIGHT} {info_color} {format}",
        logging.WARNING: f"{warning_emoji} {Style.BRIGHT} {warning_color} {format}",
        logging.ERROR: f"{error_emoji} {Style.BRIGHT} {error_color} {format}",
        logging.CRITICAL: f"{critical_emoji} {Style.BRIGHT} {critical_color} {format}"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# create logger with 'spam_application'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(ColoredOuputFormatter())

logger.addHandler(ch)
# suppress the py4j logger if its there
py4jlogger = logging.getLogger("py4j")
py4jlogger.addHandler(ch)
py4jlogger.setLevel(logging.DEBUG)