# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

from flowrunner import BaseFlow, end, start, step

spark = SparkSession.builder.getOrCreate()


class ExamplePySpark(BaseFlow):
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

        data1 = [
            ("Hermione",100),
            ("Harry", 85),
            ("Ron", 75),
        ]

        data2 =  [
            ("Hermione",100),
            ("Harry", 90),
            ("Ron", 80),
        ]

        columns = ["Name", "marks"]

        rdd1 = spark.sparkContext.parallelize(data1)
        rdd2 = spark.sparkContext.parallelize(data2)
        self.df1 = spark.createDataFrame(rdd1).toDF(*columns)
        self.df2 = spark.createDataFrame(rdd2).toDF(*columns)

    @step(next=["append_data"])
    def transformation_function_1(self):
        """
        Here we add a snapshot_date to the input dataframe of 2023-03-12
        """

        self.transformed_df_1 = self.df1.withColumn("snapshot_date", lit("2023-03-12"))

    @step(next=["append_data"])
    def transformation_function_2(self):
        """
        Here we add a snapshot_date to the input dataframe of 2023-01-01
        """
        self.transformed_df_2 = self.df2.withColumn("snapshot_date", lit("2023-01-01"))

    @step(next=["show_data"])
    def append_data(self):
        """
        Here we append the two dataframe together
        """
        self.final_df = self.transformed_df_1.union(self.transformed_df_2)

    @end
    @step
    def show_data(self):
        """
        Here we show the new final dataframe of aggregated data. However in real use cases. It would
        be more likely to write the data to some final layer/format
        """
        self.final_df.show()
        return self.final_df
