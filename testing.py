from flowrunner.runner.flow import BaseFlow
from flowrunner.core.decorators import step, start, end

class ExampleFlow(BaseFlow):
    @start
    @step(next=['method2'])
    def method1(self):
        return None

    @step(next=['method3'])
    def method2(self):
        return None

    @end
    @step
    def method3(self):
        return None


ExampleFlow().show()