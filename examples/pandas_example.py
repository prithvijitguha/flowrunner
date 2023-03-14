# -*- coding: utf-8 -*-
import pandas as pd

from flowrunner import BaseFlow, end, start, step


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
