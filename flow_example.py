from flowrunner.decorators import step, start, end
from flowrunner.core.data_store import read_output


@start
@step(next=['middle_func', 'another_middle_func'])
def first_func():
    """This function is the start of our workflow
    where we extract 3 dataframes"""
    x = 2
    return x

@step(next='model_func')
def middle_func():
    """This function is the middle where we
    filter + transform stuff"""
    value_from_first = read_output("first_func")
    return value_from_first * 3



@step(next='model_func')
def another_middle_func():
    """This function is the middle where we
    filter + transform stuff"""
    value_from_first = read_output('first_func')
    return value_from_first + 6

@step(next='end_func')
def model_func():
    """This function does model training"""
    y = read_output('middle_func')
    x = read_output('another_middle_func')
    return x - y

@end
@step
def end_func():
    """This function is the end where
    we write data into a table"""
    final_value = read_output('model_func')
    print(final_value)
    return final_value

