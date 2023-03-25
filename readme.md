# flowrunner: A lightweight Data Engineering/Science Flow package

[![codecov](https://codecov.io/gh/prithvijitguha/FlowRunner/branch/main/graph/badge.svg?token=0B8X2WF0OA)](https://codecov.io/gh/prithvijitguha/FlowRunner)&nbsp;
![build](https://github.com/prithvijitguha/FlowRunner/actions/workflows/build.yml/badge.svg?branch=main)&nbsp;
![tests](https://github.com/prithvijitguha/FlowRunner/actions/workflows/tests.yml/badge.svg?branch=main)&nbsp;
![documentation](https://github.com/prithvijitguha/FlowRunner/actions/workflows/docs.yml/badge.svg?branch=main)&nbsp;
[![Documentation Status](https://readthedocs.org/projects/flowrunner/badge/?version=latest)](https://flowrunner.readthedocs.io/en/latest/?badge=latest)&nbsp;
[![Python 3.8](https://img.shields.io/badge/python-3.8-%2334D058.svg)](https://www.python.org/downloads/release/python-380/)&nbsp;
[![Python 3.9](https://img.shields.io/badge/python-3.9-%2334D058.svg)](https://www.python.org/downloads/release/python-390/)&nbsp;
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)&nbsp;
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)&nbsp;
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## What is it?
**flowrunner** is a lightweight package to organize and represent Data Engineering/Science workflows. Its designed to be
integrated with any pre-existing framework like pandas or PySpark

## Main Features
- Lazy evaluation of DAG: flowrunner does not force you to execute/run your dag until you want to, only run it when its explicitly mentioned as `run`
- Easy syntax to build new Flows
- Easy data sharing between methods in a `Flow` using attributes
- Data store to store output of a function(incase it has `return`) for later
- Param store to easily pass reusable parameters to `Flow`
- Visualizing your flow as a DAG

## Installing flowrunner
To install flowrunner, following commands will work

Source code is hosted at https://github.com/prithvijitguha/flowRunner

```sh
$ pip install flowrunner
```

Or install from source
```sh
$ pip install git+https://github.com/prithvijitguha/flowrunner@main
```


## Usage

Here is a quick example to run as is

```python
# example.py
from flowrunner import BaseFlow, step, start, end

class ExampleFlow(BaseFlow):
    @start
    @step(next=['method2', 'method3'])
    def method1(self):
        self.a = 1

    @step(next=['method4'])
    def method2(self):
        self.a += 1

    @step(next=['method4'])
    def method3(self):
        self.a += 2

    @end
    @step
    def method4(self):
        self.a += 3
        print("output of flow is:", self.a)
```

You can run the flow with the following command
```console
$ python -m flowrunner run example.py
output of flow is: 7
```

Or in a notebook/script like this:

```python
ExampleFlow.run()
```


## Visualize Flow as DAG(Directed Acyclical Graph)

```python
ExampleFlow().display()
```

Your output will look like this.

![image](https://user-images.githubusercontent.com/71138854/227732793-d5ee52a5-a090-4b51-8b63-25e4af4909f2.png)


Or can be run in cli like this:

```sh
python -m flowrunner display example.py
```


For CLI usage we create a file called `exampleflow.html` in the current directory with the same output

## Show your Flow

```python
ExampleFlow().show()
```

```console
2023-03-08 22:35:24 LAPTOP flowrunner.system.logger[12692] INFO Found flow ExampleFlow
2023-03-08 22:35:24 LAPTOP flowrunner.system.logger[12692] DEBUG Validating flow for ExampleFlow
✅ Validated number of start nodes
✅ Validated start nodes 'next' values
✅ Validate number of middle_nodes
✅ Validated middle_nodes 'next' values
✅ Validated end nodes
✅ Validated start nodes 'next' values
2023-03-08 22:35:24 LAPTOP  flowrunner.system.logger[12692] DEBUG Show flow for ExampleFlow
method1

?
  Next=method2, method3


method2

?
  Next=method4


method3

?
  Next=method4
```

Or through CLI like below
```console
python -m flowrunner show example.py
```

## Pandas Example

```python

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
```

Now when you run `ExamplePandas().display()` you get the following output


![image](https://user-images.githubusercontent.com/71138854/227732600-7bae5e21-3c9a-4ad9-85da-f926cded2636.png)


## Documentation
Check out the latest documentation here: [FlowRunner documentation](https://flowrunner.readthedocs.io/en/latest/)

## Contributing
All contributions are welcome :smiley:

If you are interested in contributing, please check out this page: [FlowRunner Contribution Page](https://flowrunner.readthedocs.io/en/latest/contributing_guide_code.html)
