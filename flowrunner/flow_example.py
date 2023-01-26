from decorators import step, start, end, read_output
from core.data_store import DataStore

data_store = DataStore()

@start
@step(next=['middle_func', 'another_middle_func'])
def first_func():
    """This function is the start of our workflow
    where we extract 3 dataframes"""
    x = 2
    return x

@step(next='model_func')
def middle_func(data_store):
    """This function is the middle where we
    filter + transform stuff"""
    value_from_first = data_store["first_func"]
    return value_from_first * 3



@step(next='model_func')
def another_middle_func(data_store):
    """This function is the middle where we
    filter + transform stuff"""
    value_from_first = read_output('first_func')
    return value_from_first + 6

@step(next='end_func')
def model_func():
    """This function does model training"""
    y = data_store['middle_func']
    x = data_store['another_middle_func']
    return x - y

@end
@step
def end_func():
    """This function is the end where
    we write data into a table"""
    final_value = data_store['model_func']
    print(final_value)
    return final_value

