"""Module to test that cookie cutter is working as expected"""
import pytest

@pytest.fixture
def custom_template(tmpdir):
    """Function to create cookie cutter template"""
    template = tmpdir.ensure("cookiecutter-template", dir=True)
    template.join("cookiecutter.json").write('{"repo_name": "example-project"}')

    repo_dir = template.ensure("{{cookiecutter.repo_name}}", dir=True)
    repo_dir.join("README.rst").write("{{cookiecutter.repo_name}}")

    return template


def test_bake_custom_project(cookies, custom_template):
    """Test for 'cookiecutter-template'."""
    result = cookies.bake(template=str(custom_template))

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "example-project"
    assert result.project_path.is_dir()