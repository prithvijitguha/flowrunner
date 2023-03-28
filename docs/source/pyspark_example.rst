.. _pyspark_example:

PySpark example with FlowRunner
================================


.. contents:: Table of contents:
   :local:


Pre-Requisites
------------------

- :ref:`Getting started page <getting_started>`
- Install pyspark(just binaries, for detailed and complete installation refer this link `Install PySpark on Windows <https://sparkbyexamples.com/pyspark/how-to-install-and-run-pyspark-on-windows/>`_)
    .. code-block:: console

        pip install pyspark>=3.3.2


.. _pyspark_example.pre_requisites:


Example PySpark Flow
----------------------

Create the following flow inside a file called `pandas_example.py`. For this example we create a dataset, add a date for each dataset
append/union these together and then show the final dataset.


.. literalinclude:: ../../examples/pyspark_example.py
   :language: python




.. _pyspark_example.example_pyspark_flow:


Let's show our Flow
---------------------------------------------

Run the following command to show() your flow. This gives us a description based on the docstrings
of what our flow is actually going to do, without actually running it

.. tabs::

   .. group-tab::  cli

      .. code-block:: powershell

        python -m flowrunner show pandas_example.py

   .. group-tab::  Flow methods

      .. code-block:: python

        # we create an instance of the class and run its corresponding method
        ExamplePySpark().show()


You should see the following output:

.. code-block:: console

    Welcome to flowrunner!
    2023-03-12 19:50:47 LAPTOP flowrunner.system.logger[22656] INFO Found flow ExamplePySpark
    2023-03-12 19:50:47 LAPTOP flowrunner.system.logger[22656] DEBUG Validating flow for ExamplePySpark
    ✅ Validated number of start nodes
    ✅ Validated start nodes 'next' values
    ✅ Validate number of middle_nodes
    ✅ Validated middle_nodes 'next' values
    ✅ Validated end nodes
    ✅ Validated start nodes 'next' values
    2023-03-12 19:50:47 LAPTOP flowrunner.system.logger[22656] DEBUG Show flow for ExamplePySpark
    create_data


            This method we create the dataset we are going use. In real use cases,
            you'll have to read from a source (csv, parquet, etc)

            For this example we create two dataframes for students ranked by marked scored
            for when they attempted the example on 1st January 2023 and 12th March 2023

            After creating the dataset we pass it to the next methods

            - transformation_function_1
            - transformation_function_2

    Next=transformation_function_1, transformation_function_2


    transformation_function_2


            Here we add a snapshot_date to the input dataframe of 2023-01-01

    Next=append_data


    transformation_function_1


            Here we add a snapshot_date to the input dataframe of 2023-03-12

    Next=append_data


    append_data


            Here we append the two dataframe together

    Next=show_data


    show_data


            Here we show the new final dataframe of aggregated data. However in real use cases. It would
            be more likely to write the data to some final layer/format


.. _pyspark_example.show:



Display our Flow
-------------------

This requires IPython style interactive notebooks

.. tabs::

   .. group-tab::  cli

      .. code-block:: powershell

        python -m flowrunner display pandas_example.py

   .. group-tab::  Flow methods

      .. code-block:: python

        # we create an instance of the class and run its corresponding method
        ExamplePySpark().display()


.. image:: https://user-images.githubusercontent.com/71138854/227732600-7bae5e21-3c9a-4ad9-85da-f926cded2636.png
  :width: 1500
  :alt: Display DAG Flow



.. _pyspark_example.display:


Run our Flow
--------------

Now that we have an idea of what our Flow is going to do, let's actually run it.

The following command will run the flow

.. tabs::

   .. group-tab::  cli

      .. code-block:: powershell

        python -m flowrunner run pandas_example.py

   .. group-tab::  Flow methods

      .. code-block:: python

        # we create an instance of the class and run its corresponding method
        ExamplePySpark().run()


You should see the following output

.. code-block:: console

    2023-03-12 19:54:12 LAPTOP DEBUG Validating flow for ExamplePySpark
    2023-03-12 19:54:12 LAPTOP WARNING Validation will raise InvalidFlowException if invalid Flow found
    ✅ Validated number of start nodes
    ✅ Validated start nodes 'next' values
    ✅ Validate number of middle_nodes
    ✅ Validated middle_nodes 'next' values
    ✅ Validated end nodes
    ✅ Validated start nodes 'next' values
    2023-03-12 19:54:12 LAPTOP DEBUG Running flow for ExamplePySpark
            Name snapshot_date  marks
    rank1  Hermione    2023-03-12    100
    rank2     Harry    2023-03-12     85
    rank3       Ron    2023-03-12     75
    rank1  Hermione    2023-01-01    100
    rank2       Ron    2023-01-01     90


.. _pyspark_example.run:



Conclusion
--------------

You're all set! You can whatever you would like to this Flow as per your use case!

Additional Resources: :ref:`Notebook Examples(Including Pyspark and Databricks Notebooks) <notebook_examples>`


.. _pyspark_example.conclusion:
