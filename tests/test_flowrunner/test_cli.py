# -*- coding: utf-8 -*-
"""Commands to check the cli"""

from click.testing import CliRunner

from flowrunner.cli import flowchart, run, show, validate


def test_validate():
    runner = CliRunner()
    result = runner.invoke(validate, ["examples/example.py"])
    assert result.exit_code == 0


def test_show():
    runner = CliRunner()
    result = runner.invoke(show, ["examples/example.py"])
    assert result.exit_code == 0


def test_run():
    runner = CliRunner()
    result = runner.invoke(run, ["examples/example.py"])
    assert result.exit_code == 0


def generate_flowchart():
    runner = CliRunner()
    result = runner.invoke(flowchart, ["examples/example.py"])
    assert result.exit_code == 0
