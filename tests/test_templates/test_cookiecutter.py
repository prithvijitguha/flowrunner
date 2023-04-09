# -*- coding: utf-8 -*-
import pytest


@pytest.mark.skip("Test not ready, placeholder for cookiecutter")
def test_bake_project(cookies):
    result = cookies.bake(extra_context={"repo_name": "helloworld"})

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "helloworld"
    assert result.project_path.is_dir()

    # The `project` attribute is deprecated
    assert result.project.basename == "helloworld"
    assert result.project.isdir()
