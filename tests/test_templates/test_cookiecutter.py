# -*- coding: utf-8 -*-
"""Module to test that cookie cutter is working as expected"""

def test_bake_project(cookies):
    result = cookies.bake()

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == "Flowrunner_Project_Simple"
    assert result.project.isdir()
