from decorators import step, start, end


@step(next='middle_func')
def first_func():
    """This function is the start of our workflow
    where we extract 3 dataframes"""
    print("hello world first")


@step(next='adsasd')
def middle_func():
    """This function is the middle where we
    filter + transform stuff"""
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

