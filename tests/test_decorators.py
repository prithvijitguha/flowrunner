from flowrunner.decorators import step
import pytest

@pytest.fixture
@step
def test_function():
    return None

def test_step():
    """A function to check where the step decorator works as required"""
    assert hasattr(test_function, 'name')
    assert hasattr(test_function, 'next')
    assert hasattr(test_function, 'is_step')
    assert test_function.name == test_function.__name__
    assert test_function.is_step == True


