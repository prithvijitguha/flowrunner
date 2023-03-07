.. _creating_development_environment:

Creating Your Development Environment
=======================================

.. contents:: Table of contents:
   :local:

Pre-Requisites
------------------
For FlowRunner we will require the following
- Python Version >= 3.9
You can check your python version with the following command
.. code-block:: powershell

    python --version

You can install Python from here `Python Language Home Page <https://www.python.org/>`_

- venv python package(we use venv but please feel free to virtualenv or other virtual environment)

.. code-block:: powershell

    pip install venv


Step 1: create an isolated environment
----------------------------------------

Before we begin, please:

* Make sure that you have :any:`cloned and forked the repository <contributing_guide_code.forking>`
* ``cd`` to the FlowRunner source directory

**Windows**

.. code-block:: powershell

    python -m venv flow_dev
    flow_dev/scripts/activate

**Linux**

.. code-block:: bash

    python -m venv flow_dev
    source flow_dev/bin/activate



Step 2: Install the required packages
----------------------------------------

Install the required packages using pip

**Editable Install**

.. code-block:: powershell

    pip install -e .

**Install Development Packages**

.. code-block:: powershell

    pip install -e .[dev]

**Install Testing Packages**

.. code-block:: powershell

    pip install -e .[test]


**Install Documentation Packages**

.. code-block:: powershell

    pip install -e .[doc]



.. note::
   You will need to repeat the step each time you have made a change to the codebase
