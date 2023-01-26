from flowrunner.decorators import step, start, end, Step
import pytest

@pytest.fixture
def test_function():
    return None

@pytest.fixture
def test_function():
    return None


@pytest.fixture
@start
@step
def test_start_function():
    return None


@pytest.fixture
@end
@step
def test_end_function():
    return None


def test_step():
    """A function to check where the step decorator works as required"""
    assert hasattr(test_function, 'name')
    assert hasattr(test_function, 'next')
    assert hasattr(test_function, 'is_step')
    assert test_function.name == test_function.__name__
    assert test_function.is_step == True



def test_start():
    """A function to check the start decorator"""
    assert hasattr(test_start_function, 'is_start')
    assert test_start_function.is_start == True


def test_end():
    """A function to check the end decorator"""
    assert hasattr(test_end_function, 'is_end')
    assert test_end_function.is_end == True