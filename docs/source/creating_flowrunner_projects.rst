.. _creating_flowrunner_projects:

Creating Flowrunner Project
===================================

.. contents:: Table of contents:
   :local:

What is a Flowrunner Project
------------------------------

A flowrunner project is a cookiecutter project template to get started saving and running your flows

.. _creating_flowrunner_projects.what_is_a_flowrunner_project:


Project Directory
--------------------

This is what the project directory looks like


| my_flowrunner_project
| ├── my_flowrunner_src: `the source directory`
| │ ├── html_dags: `Html visualizations of your python flows`
| │ ├── my_flows: `A directory of your flows`
| ├── docs: `A folder to store technical documentation`
| │ ├── source
| │ ├── make.bat
| │ ├── Makefile
| │ └── source
| ├── README.md: `Details about the project, install, usage, etc`
| ├── pyproject.toml `Project toml to define dependencies`
| └── changelog.md: `A markdown file to track changes`
| └── setup.py: `Backwards compatibility for older python versions`

.. _creating_flowrunner_projects.project_directory:


Usage
-------

.. code-block:: bash

    flowrunner init


.. _creating_flowrunner_projects.usage:
