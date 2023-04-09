# {{ cookiecutter.project_name }}

[![Python 3.8](https://img.shields.io/badge/python-3.8-%2334D058.svg)](https://www.python.org/downloads/release/python-380/)&nbsp;
[![Python 3.9](https://img.shields.io/badge/python-3.9-%2334D058.svg)](https://www.python.org/downloads/release/python-390/)&nbsp;

## What is it?
**{{ cookiecutter.project_slug }}** is a project to create and store flows for ETL workflows. Its based on the flowrunner
package

{{ cookiecutter.description }}

![flowrunner](https://github.com/prithvijitguha/flowrunner)


## Installing flowrunner
To install flowrunner, following commands will work

Source code is hosted at https://github.com/prithvijitguha/flowRunner

```sh
pip install {{ cookiecutter.project_slug }}
```


## Create flows
```sh
python -m flowrunner display-dir myflows --path='html_dags'
```
