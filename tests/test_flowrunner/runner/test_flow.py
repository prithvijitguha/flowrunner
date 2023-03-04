from flowrunner.runner.flow import BaseFlow, FlowRunner
from flowrunner.core.decorators import step, start, end


class FlowExample(BaseFlow):
    @start
    @step(next=['middle_func', 'another_middle_func'])
    def first_func(self):
        """This function is the start of our workflow
        where we extract 3 dataframes"""
        x = 2
        self.data_store['first_func'] = x
        print("first_func output", x)

    @step(next='model_func')
    def middle_func(self):
        """This function is the middle where we
        filter + transform stuff"""
        value_from_first = self.data_store['first_func']
        self.data_store['middle_func'] = value_from_first * 3
        print("middle_func output", self.data_store['middle_func'])



    @step(next='model_func')
    def another_middle_func(self):
        """This function is the middle where we
        filter + transform stuff"""

        value_from_first = self.data_store['first_func']
        self.data_store['another_middle_func'] = value_from_first
        print("another_middle_func output", value_from_first)

    @step(next='end_func')
    def model_func(self):
        """This function does model training"""
        y = self.data_store['middle_func']
        x = self.data_store['another_middle_func']
        self.data_store['model_func'] = x + y
        print("model_func output", x)
        print("model_func output", y)



    @end
    @step
    def end_func(self):
        """This function is the end where
        we write data into a table"""
        final_value = self.data_store['model_func']
        print("end_func output", final_value)



def test_validate_flow():
    """Run validate flow"""
    FlowExample().validate_flow()


def test_validate_flow_with_error():
    FlowExample().validate_flow_with_error() # we validate the flow and throw an exception if its not valid


def test_flowrunner():
    flow_runner = FlowRunner(FlowExample)
    flow_runner.run_flow()

def test_base_flow_run_flow():
    FlowExample().run_flow()



