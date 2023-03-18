# -*- coding: utf-8 -*-
"""Welcome to FlowRunner!

FlowRunner is a lightweight package to organize and represent Data Engineering/Science workflows. Its designed to be
integrated with any pre-existing framework like pandas or PySpark

Main Features
- Easy BaseFlow to use to build Flows off of
- Simple decorators to convert methods to Flow methods
- Command Line Interface for running Flows


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
        print(self.a)
```

You can run the flow with the following command
```sh
$ python -m flowrunner example.py
7
```
"""

from flowrunner.core.decorators import end, start, step
from flowrunner.runner.flow import BaseFlow, FlowRunner
