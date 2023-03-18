.. _creating_development_environment:

Creating Your Development Environment
=======================================

.. contents:: Table of contents:
   :local:

Pre-Requisites
------------------
For FlowRunner we will require the following
* Python Version >= 3.9. You can check your python version with the following command

    .. code-block:: powershell

        python --version

.. note:: You can install Python from here `Python Language Home Page <https://www.python.org/>`_

* venv python package(we use venv but please feel free to virtualenv or other virtual environment)

    .. code-block:: powershell

        pip install venv


.. _creating_development_environment.pre_requisites:

Step 1: create an isolated environment
----------------------------------------

Before we begin, please:

* Make sure that you have :ref:`cloned and forked the repository <contributing_guide_code.forking>`
* ``cd`` to the FlowRunner source directory

.. tabs::
    .. group-tab:: Windows

        .. code-block:: powershell

            python -m venv flow_dev
            flow_dev/scripts/activate


    .. group-tab:: Unix/macOS

        .. code-block:: bash

            python -m venv flow_dev
            source flow_dev/bin/activate


.. _creating_development_environment.create_env:

Step 2: Install the required packages
----------------------------------------

Install the required packages using `pip`

Following are commands depending on what part of FlowRunner you are working on

The `-e` or `--editable` creates an editable installation of `flowrunner` so you can make changes and test your code with a
faster feedback loop

.. code-block:: powershell

    pip install -e .

.. tabs::

    .. group-tab:: **Install Development Packages**

        .. code-block:: powershell

            pip install -e .[dev]

    .. group-tab:: **Install Testing Packages**

        .. code-block:: powershell

            pip install -e .[test]

    .. group-tab:: **Install Documentation Packages**

        .. code-block:: powershell

            pip install -e .[doc]
