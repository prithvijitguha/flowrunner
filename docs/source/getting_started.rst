.. _getting_started:

.. role:: python(code)
  :language: python
  :class: highlight

.. role:: bash(code)
  :language: bash
  :class: highlight

Getting Started
====================

.. contents:: Table of contents:
   :local:



Installing FlowRunner
--------------------------

Currently FlowRunner is available through PyPI

.. code-block:: powershell

   pip install flowrunner


To install the latest development version


.. code-block:: powershell

    pip install git+https://github.com/prithvijitguha/flowrunner@main

.. _getting_started.installing_flowrunner:

Quickstart
---------------

Create your first ``Flow``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a file called ``example.py`` containing the below code. Make sure to ``cd`` to same the directory that
contains ``example.py``



.. literalinclude:: ../../examples/example.py
   :language: python

.. _getting_started.create_first_flow:


Working with your Flow
-------------------------

Flows can be run in two ways:

* cli: The command line interface way :bash:`python -m flowrunner [COMMAND] [PATH_TO_FLOW_FILE.py]`
* Flow methods: The inbuilt class methods :python:`ExampleFlow().insert_method_name()`


``validate`` your Flow
^^^^^^^^^^^^^^^^^^^^^^

We run ``validate`` to validate our Flow

.. tabs::

   .. group-tab::  cli

      .. code-block:: powershell

         python -m flowrunner validate example.py

   .. group-tab::  Flow methods

      .. code-block:: python

         # we create an instance of the class and run its corresponding method
         ExampleFlow().validate()


The output runs validation checks on your Flow with ✅ for passed and ❌ for failed

.. code-block:: console

   2023-03-08 22:36:58 LAPTOP flowrunner.system.logger[9008] INFO Found flow ExampleFlow
   2023-03-08 22:36:58 LAPTOP flowrunner.system.logger[9008] DEBUG Validating flow for ExampleFlow
   ✅ Validated number of start nodes
   ✅ Validated start nodes 'next' values
   ✅ Validate number of middle_nodes
   ✅ Validated middle_nodes 'next' values
   ✅ Validated end nodes
   ✅ Validated start nodes 'next' values



.. _getting_started.validate_flow:


``display`` your Flow
^^^^^^^^^^^^^^^^^^^^^^

We can use ``display`` command to visualize your Flow DAG in a notebook or the CLI to save it to the current folder

.. tabs::
   .. group-tab::  cli

      .. code-block:: powershell

         python -m flowrunner display example.py

   .. group-tab::  Flow methods

      .. code-block:: python

         # we create an instance of the class and run its corresponding method
         ExampleFlow().display()


.. mermaid::

    graph TD;
        method_1(method_1) --> method_2(method_2);
        method_1(method_1) --> method_3(method_3);
        method_2(method_2) --> method_4(method_4);
        method_3(method_3) --> method_4(method_4);


.. _getting_started.display:



``show`` your Flow
^^^^^^^^^^^^^^^^^^^^^^

We can use ``show`` command to display the order of iteration of our flow with description of each
step based on the docstring of the function

Output will look like this. `"?"` is used in absence of a docstring for the method. However if you add a docstring
that will show up too!

.. tabs::

   .. group-tab::  cli

      .. code-block:: powershell

         python -m flowrunner show example.py

   .. group-tab::  Flow methods

      .. code-block:: python

         # we create an instance of the class and run its corresponding method
         ExampleFlow().show()



.. code-block:: console

   2023-03-08 22:35:24 LAPTOP flowrunner.system.logger[12692] INFO Found flow ExampleFlow
   2023-03-08 22:35:24 LAPTOP flowrunner.system.logger[12692] DEBUG Validating flow for ExampleFlow
   ✅ Validated number of start nodes
   ✅ Validated start nodes 'next' values
   ✅ Validate number of middle_nodes
   ✅ Validated middle_nodes 'next' values
   ✅ Validated end nodes
   ✅ Validated start nodes 'next' values
   2023-03-08 22:35:24 LAPTOP  flowrunner.system.logger[12692] DEBUG Show flow for ExampleFlow
   method1

   ?
      Next=method2, method3


   method2

   ?
      Next=method4


   method3

   ?
      Next=method4


   method4

   ?
      Next=


.. _getting_started.show_flow:

``run`` your Flow
^^^^^^^^^^^^^^^^^^^^^^

We can use ``run`` command to actually run the flow

.. tabs::
   .. group-tab::  cli

      .. code-block:: powershell

         python -m flowrunner run example.py

   .. group-tab::  Flow methods

      .. code-block:: python

         # we create an instance of the class and run its corresponding method
         ExampleFlow().run()


.. code-block:: console

   2023-03-08 22:29:48 LAPTOP flowrunner.system.logger[13528] INFO Found flow ExampleFlow
   2023-03-08 22:29:48 LAPTOP flowrunner.system.logger[13528] DEBUG Validating flow for ExampleFlow
   2023-03-08 22:29:48 LAPTOP flowrunner.system.logger[13528] WARNING Validation will raise InvalidFlowException if invalid Flow found
   ✅ Validated number of start nodes
   ✅ Validated start nodes 'next' values
   ✅ Validate number of middle_nodes
   ✅ Validated middle_nodes 'next' values
   ✅ Validated end nodes
   ✅ Validated start nodes 'next' values
   2023-03-08 22:29:48 LAPTOP flowrunner.system.logger[13528] DEBUG Running flow for ExampleFlow
   7


.. _getting_started.run_flow:
