# -*- coding: utf-8 -*-
"""Commands to check the cli"""

from click.testing import CliRunner

from flowrunner.cli import cli, flowchart, run, show, validate


def test_validate():
    """Test to check cli::validate function"""
    runner = CliRunner()
    result = runner.invoke(validate, ["examples/example.py"])
    assert result.exit_code == 0


def test_show():
    runner = CliRunner()
    result = runner.invoke(show, ["examples/example.py"])
    assert result.exit_code == 0


def test_run():
    """Test to check cli::run function"""
    runner = CliRunner()
    result = runner.invoke(run, ["examples/example.py"])
    assert result.exit_code == 0


def test_flowchart():
    """Test to check cli::flowchart function"""
    runner = CliRunner()
    result = runner.invoke(
        flowchart, ["examples/example.py", "--path=example_flowchart/"]
    )
    assert result.exit_code == 0


def test_cli():
    """Test to check cli::cli function"""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
