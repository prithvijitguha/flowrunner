from flowrunner.decorators import step, start, end
from flowrunner.core.graph import BaseFlow




class FlowExample(BaseFlow):
    @start
    @step(next=['middle_func', 'another_middle_func'])
    def first_func():
        """This function is the start of our workflow
        where we extract 3 dataframes"""
        x = 2
        return x

    @step(next='model_func')
    def middle_func(self):
        """This function is the middle where we
        filter + transform stuff"""
        value_from_first = self.read_output("first_func")
        return value_from_first * 3



    @step(next='model_func')
    def another_middle_func(self):
        """This function is the middle where we
        filter + transform stuff"""
        value_from_first = self.read_output('first_func')
        return value_from_first + 6

    @step(next='end_func')
    def model_func(self):
        """This function does model training"""
        y = self.read_output('middle_func')
        x = self.read_output('another_middle_func')
        return x - y

    @end
    @step
    def end_func(self):
        """This function is the end where
        we write data into a table"""
        final_value = self.read_output('model_func')
        print(final_value)
        return final_value

