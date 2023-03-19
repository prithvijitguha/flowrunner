# -*- coding: utf-8 -*-
import pytest

from flowrunner.system.logger import logger


@pytest.fixture(scope="module")
def fixture_logger():
    """Fixture to run logging methods"""
    return logger


def test_logger_output(fixture_logger, caplog):
    fixture_logger.info("hello world info")
    fixture_logger.warning("hello world warn")
    fixture_logger.debug("hello world debug")
    fixture_logger.error("hello world error")
    pytest.approx(
        caplog.records[0].msg,
        "INFO     hello world info  flowrunner.system.logger:test_logger.py:13",
    )
    pytest.approx(
        caplog.records[1].msg,
        "WARNING  hello world warn  flowrunner.system.logger:test_logger.py:14",
    )
    pytest.approx(
        caplog.records[2].msg,
        "DEBUG    hello world debug  flowrunner.system.logger:test_logger.py:15",
    )
    pytest.approx(
        caplog.records[3].msg,
        "ERROR    hello world error  flowrunner.system.logger:test_logger.py:16",
    )
