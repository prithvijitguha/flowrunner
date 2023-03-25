# Change Log

## 0.1.0 (2023-03-21)

### What is it?

flowrunner is a lightweight package to organize and represent Data Engineering/Science workflows. Its designed to be integrated with any pre-existing framework like pandas or PySpark

### Main Features
- Lazy evaluation of DAG: flowrunner does not force you to execute/run your dag until you want to, only run it when its explicitly mentioned as run
- Easy syntax to build new Flows
- Easy data sharing between methods in a Flow using attributes
- Data store to store output of a function(incase it has return) for later
- Param store to easily pass reusable parameters to Flow
- Visualizing your flow as a DAG



## 0.2.0 (2023-03-25)

### Features:
- Improved DAG visualization with description with option to turn off description
- Improved style of DAG visualization

### Documentation:
- Improved documentation for readme
- Improved example usage for pandas
