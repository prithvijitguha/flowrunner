.. _pandas_example:

Pandas example with FlowRunner
================================


.. contents:: Table of contents:
   :local:


Pre-Requisites
------------------

- :ref:`Getting started page <getting_started>`
- Install pandas
    .. code-block:: console

        pip install pandas>=1.5.3




.. _pandas_example.pre_requisites:


Example Pandas Flow
----------------------

Create the following flow inside a file called `pandas_example.py`. For this example we create a dataset, add a date for each dataset
append/union these together and then show the final dataset.


.. literalinclude:: ../../examples/pandas_example.py
   :language: python




.. _pandas_example.example_pandas_flow:


Let's show our Flow
---------------------------------------------

Run the following command to show() your flow. This gives us a description based on the docstrings
of what our flow is actually going to do, without actually running it

.. code-block:: powershell

    python -m flowrunner show pandas_example.py


You should see the following output:

.. code-block:: console

    Welcome to flowrunner!
    2023-03-12 19:50:47 LAPTOP flowrunner.system.logger[22656] INFO Found flow ExamplePandas
    2023-03-12 19:50:47 LAPTOP flowrunner.system.logger[22656] DEBUG Validating flow for ExamplePandas
    ✅ Validated number of start nodes
    ✅ Validated start nodes 'next' values
    ✅ Validate number of middle_nodes
    ✅ Validated middle_nodes 'next' values
    ✅ Validated end nodes
    ✅ Validated start nodes 'next' values
    2023-03-12 19:50:47 LAPTOP flowrunner.system.logger[22656] DEBUG Show flow for ExamplePandas
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


.. _pandas_example.show:

Run our Flow
--------------

Now that we have an idea of what our Flow is going to do, let's actually run it.

The following command will run the flow

.. code-block:: powershell

    python -m flowrunner run pandas_example.py


You should see the following output

.. code-block:: console

    2023-03-12 19:54:12 LAPTOP DEBUG Validating flow for ExamplePandas
    2023-03-12 19:54:12 LAPTOP WARNING Validation will raise InvalidFlowException if invalid Flow found
    ✅ Validated number of start nodes
    ✅ Validated start nodes 'next' values
    ✅ Validate number of middle_nodes
    ✅ Validated middle_nodes 'next' values
    ✅ Validated end nodes
    ✅ Validated start nodes 'next' values
    2023-03-12 19:54:12 LAPTOP DEBUG Running flow for ExamplePandas
            Name snapshot_date  marks
    rank1  Hermione    2023-03-12    100
    rank2     Harry    2023-03-12     85
    rank3       Ron    2023-03-12     75
    rank1  Hermione    2023-01-01    100
    rank2       Ron    2023-01-01     90


.. _pandas_example.run:

Display our Flow
-------------------

This requires IPython style interactive notebooks

.. code-block:: python

    ExamplePandas().display()


.. mermaid::

    graph TD;
        create_data(create_data) --> transformation_function_1(transformation_function_1);
        create_data(create_data) --> transformation_function_2(transformation_function_2);
        transformation_function_1(transformation_function_1) --> append_data(append_data);
        transformation_function_2(transformation_function_2) --> append_data(append_data);
        append_data(append_data) --> show_data(show_data);




Conclusion
--------------

You're all set! You can whatever you would like to this Flow as per your use case!


.. _pandas_example.conclusion:
