from decorators import step
from core.data_store import DataStore

data_store = DataStore()

@step(next='middle_func')
def first_func():
    """This function is the start of our workflow
    where we extract 3 dataframes"""
    data_store.store_data('key', 'value1')
    print("hello world first")


@step(next='model_func')
def middle_func():
    """This function is the middle where we
    filter + transform stuff"""
    print(data_store.read_data('key'))
    print("hello world middle")

@step(next='end_func')
def model_func():
    """This function does model training"""
    print("hello world model training")


@step
def end_func():
    """This function is the end where
    we write data into a table"""
    print("hello world end")

