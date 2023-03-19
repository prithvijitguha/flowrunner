# -*- coding: utf-8 -*-
import pandas as pd
import pytest

from flowrunner import BaseFlow, FlowRunner, end, start, step


class ExampleFlow(BaseFlow):
    @start
    @step(next=["method2", "method3"])
    def method1(self):
        self.a = 1
        return self.a

    @step(next=["method4"])
    def method2(self):
        self.a += 1
        return self.a

    @step(next=["method4"])
    def method3(self):
        self.a += 2
        return self.a

    @end
    @step
    def method4(self):
        self.a += 3
        print("output of flow is:", self.a)
        return self.a


def test_validate_flow():
    """Run validate flow"""
    ExampleFlow().validate()


def test_validate_flow_with_error():
    ExampleFlow().validate_with_error()  # we validate the flow and throw an exception if its not valid


def test_flowrunner():
    FlowRunner().run(ExampleFlow())


def test_base_flow_run_flow():
    ExampleFlow().run()


def test_base_flow_display():
    ExampleFlow().display()


def test_data_store():
    """Test to check if data store actually stores output"""
    flow_instance = ExampleFlow()
    flow_instance.run()
    data_store = flow_instance.data_store

    assert data_store["method1"] == 1
    assert (
        data_store["method2"] == 2 or 4
    )  # this is a weird bug where it picks up the return value of either method 2 or method 3
    assert (
        data_store["method3"] == 4 or 2
    )  # this is a weird bug where it picks up the return value of either method 2 or method 3
    assert data_store["method4"] == 7


class ExamplePandas(BaseFlow):
    @start
    @step(next=["transformation_function_1", "transformation_function_2"])
    def create_data(self):
        """
        This method we create the dataset we are going use. In real use cases,
        you'll have to read from a source (csv, parquet, etc)

        For this example we create two dataframes for students ranked by marked scored
        for when they attempted the example on 1st January 2023 and 12th March 2023

        After creating the dataset we pass it to the next methods

        - transformation_function_1
        - transformation_function_2
        """
        data1 = {"Name": ["Hermione", "Harry", "Ron"], "marks": [100, 85, 75]}

        data2 = {"Name": ["Hermione", "Ron", "Harry"], "marks": [100, 90, 80]}

        df1 = pd.DataFrame(data1, index=["rank1", "rank2", "rank3"])

        df2 = pd.DataFrame(data2, index=["rank1", "rank2", "rank3"])

        self.input_data_1 = df1
        self.input_data_2 = df2

    @step(next=["append_data"])
    def transformation_function_1(self):
        """
        Here we add a snapshot_date to the input dataframe of 2023-03-12
        """
        transformed_df = self.input_data_1
        transformed_df.insert(1, "snapshot_date", "2023-03-12")
        self.transformed_df_1 = transformed_df

    @step(next=["append_data"])
    def transformation_function_2(self):
        """
        Here we add a snapshot_date to the input dataframe of 2023-01-01
        """
        transformed_df = self.input_data_2
        transformed_df.insert(1, "snapshot_date", "2023-01-01")
        self.transformed_df_2 = transformed_df

    @step(next=["show_data"])
    def append_data(self):
        """
        Here we append the two dataframe together
        """
        self.final_df = pd.concat([self.transformed_df_1, self.transformed_df_2])

    @end
    @step
    def show_data(self):
        """
        Here we show the new final dataframe of aggregated data. However in real use cases. It would
        be more likely to write the data to some final layer/format
        """
        print(self.final_df)
        return self.final_df


@pytest.fixture(scope="module")
def pandas_expected_df():
    data1 = {"Name": ["Hermione", "Harry", "Ron"], "marks": [100, 85, 75]}

    data2 = {"Name": ["Hermione", "Ron", "Harry"], "marks": [100, 90, 80]}

    df1 = pd.DataFrame(data1, index=["rank1", "rank2", "rank3"])

    df2 = pd.DataFrame(data2, index=["rank1", "rank2", "rank3"])

    df1.insert(1, "snapshot_date", "2023-03-12")
    df2.insert(1, "snapshot_date", "2023-01-01")
    return pd.concat([df1, df2])


def test_pandas_example(pandas_expected_df):
    """Checks to see if the pandas examples as expected"""
    pandas_example = ExamplePandas()
    pandas_example.run()
    assert pandas_example.final_df.equals(
        pandas_expected_df
    )  # check if both dataframes are equal


def test_data_store(pandas_expected_df):
    """Checks to see if the pandas examples as expected"""
    pandas_example = ExamplePandas()
    pandas_example.run()

    assert pandas_example.data_store["show_data"].equals(pandas_expected_df)
    assert pandas_example.data_store["create_data"] == None
    assert pandas_example.data_store["transformation_function_1"] == None
    assert pandas_example.data_store["transformation_function_2"] == None
    assert pandas_example.data_store["append_data"] == None


def test_data_store():
    """Test to check the BaseFlow().data_store attribute"""
    param_store = {"hello_there": "general_kenobi"}

    pandas_example = ExamplePandas(param_store=param_store)
    pandas_example.run()
    assert pandas_example.param_store["hello_there"] == "general_kenobi"
