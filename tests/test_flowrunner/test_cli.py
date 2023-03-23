# -*- coding: utf-8 -*-
"""Commands to check the cli"""

import pytest
from click.testing import CliRunner

from flowrunner.cli import cli, display, run, show, validate


@pytest.fixture(scope="session")
def temp_directory_fixture(tmp_path_factory):
    folder = tmp_path_factory.mktemp("example_flowchart")
    return folder

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


def test_display(temp_directory_fixture):
    """Test to check cli::flowchart function, we use a temporary directory
    fixture for saving"""
    runner = CliRunner()
    result = runner.invoke(
        display, ["examples/example.py", f"--path={temp_directory_fixture}"]
    )
    assert result.exit_code == 0

def test_display_description(temp_directory_fixture):
    """Test to check cli::flowchart function, we use a temporary directory
    fixture for saving. We use the description flag"""
    runner = CliRunner()
    result = runner.invoke(
        display, ["examples/example.py", f"--path={temp_directory_fixture}", f"--description={True}"]
    )
    assert result.exit_code == 0


def test_cli():
    """Test to check cli::cli function"""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
