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


## 0.2.1 (2023-04-02)

### Features:
- Improved checks for cyclic flows
- Support for PySpark `pip install flowrunner[pyspark]`
- Improved validation for stranded middle origin nodes

### Documentation:
- Changed theme to sphinx_the_docs
- Added API reference documentation
- Improved documentation examples with Databricks and PySpark


## 0.2.2 (2023-06-03)

### Features:
- Add cookie cutter template
- Improved logging

### Documentation:
- Fixed broken notebook example links
