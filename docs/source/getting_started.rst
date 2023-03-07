.. _getting_started:

Getting Started
====================

.. contents:: Table of contents:
   :local:


Installing FlowRunner
--------------------------

Currently FlowRunner is only available through source

.. code-block:: powershell

    pip install git+https://github.com/prithvijitguha/FlowRunner@main



Quickstart
---------------

Create your first ``Flow``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a file called ``example.py`` containing the below code. Make sure to ``cd`` to same the directory that
contains ``example.py``


.. code-block:: python

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


``validate`` your Flow
^^^^^^^^^^^^^^^^^^^^^^

We run ``validate`` to validate our Flow

.. code-block:: powershell

   python -m flowrunner validate example.py


``show`` your Flow
^^^^^^^^^^^^^^^^^^^^^^

We can use ``show`` command to display the order of iteration of our flow with description of each
step based on the docstring of the function

.. code-block:: powershell

   python -m flowrunner show example.py


``run`` your Flow
^^^^^^^^^^^^^^^^^^^^^^

We can use ``run`` command to actually run the flow

.. code-block:: powershell

   python -m flowrunner run example.py
   7
