.. _introduction:

Welcome to flowrunner
==========================

.. contents:: Table of contents:
   :local:


Introduction
-----------------

flowrunner is a lightweight package to organize and represent Data Engineering/Science workflows. Its designed to be
integrated with any pre-existing framework like pandas or PySpark


.. _introduction.intro:

Concepts
^^^^^^^^^^^^^^^^^^^^^^^

- **Flow**: A collection of all the functions you want to run, organized in way you want them to run, subclassed from `BaseFlow`
- **DAG**: A Directed Acyclic Graph is a type of graph that is directed and without cycles connecting the other edges, meaning that it has a clear start and end node
- **flowrunner DAG**: A dag we use to keep track and visualize the order of execution of a Flow


.. _introduction.concepts:

What is flowrunner
^^^^^^^^^^^^^^^^^^^^^^^
flowrunner in essence is a way to write quick ETL(Extract, Transform, Load)/Data WorkFlows in the form of a Directed Acyclical Graph called a `Flow`

.. _introduction.what:


Why flowrunner
^^^^^^^^^^^^^^^^
FlowRunner is easy and lightweight and can fit on top of any existing framework like PySpark or Pandas. This addresses things that Airflow has trouble with like sharing
data between tasks/dags through XCOM which limits to string format.

.. _introduction.why:


What flowrunner is not?
^^^^^^^^^^^^^^^^^^^^^^^^^^
An orchestrator, flowrunner handles no part of the scheduling, it is recommneded to use it within another scheduler orchestrator like Airflow


.. _introduction.what_not:


Features
^^^^^^^^^^^^^^

- Lazy evaluation of DAG: flowrunner does not force you to execute/run your dag until you want to, only run it when its explicitly mentioned as `run`
- Easy syntax to build new Flows
- Easy data sharing between methods in a `Flow` using attributes
- Data store to store output of a function(incase it has `return`) for later
- Param store to easily pass reusable parameters to `Flow`
- Visualizing your flow as a DAG

.. _introduction.features:
