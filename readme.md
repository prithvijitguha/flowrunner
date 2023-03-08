# FlowRunner: A lightweight Data Engineering/Science Flow package

[![codecov](https://codecov.io/gh/prithvijitguha/FlowRunner/branch/main/graph/badge.svg?token=0B8X2WF0OA)](https://codecov.io/gh/prithvijitguha/FlowRunner)
![tests](https://github.com/prithvijitguha/FlowRunner/actions/workflows/tests.yml/badge.svg?branch=main)&nbsp;
![build](https://github.com/prithvijitguha/FlowRunner/actions/workflows/build.yml/badge.svg?branch=main)&nbsp;
[![Documentation Status](https://readthedocs.org/projects/flowrunner/badge/?version=latest)](https://flowrunner.readthedocs.io/en/latest/?badge=latest)
[![Python 3.9](https://img.shields.io/badge/python-3.9-%2334D058.svg)](https://www.python.org/downloads/release/python-390/)&nbsp;
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)&nbsp;
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)&nbsp;

## What is it?
**FlowRunner** is a lightweight package to organize and represent Data Engineering/Science workflows. Its designed to be
integrated with any pre-existing framework like pandas or PySpark

## Main Features
- Easy BaseFlow to use to build Flows off of
- Simple decorators to convert methods to Flow methods
- Command Line Interface for running Flows

## Installing FlowRunner
To install FlowRunner, following commands will work

Source code is hosted at https://github.com/prithvijitguha/FlowRunner

```sh
$ pip install git+https://github.com/prithvijitguha/FlowRunner@main
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
```sh
$ python -m flowrunner run example.py
output of flow is: 7
```

## Documentation
Check out the latest documentation here: [FlowRunner documentation](https://flowrunner.readthedocs.io/en/latest/)

## Contributing
All contributions are welcome :smiley:

If you are interested in contributing, please check out this page: [FlowRunner Contribution Page](https://flowrunner.readthedocs.io/en/latest/contributing_guide_code.html)
