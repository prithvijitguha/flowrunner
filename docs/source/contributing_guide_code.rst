.. _contributing_guide_code:

Contributing Guide - Code
===================================

.. contents:: Table of contents:
   :local:

Where to start?
-----------------

- An easy way to start is to check the issues `flowrunner issues page <https://github.com/prithvijitguha/flowrunner/issues>`_
- Adding test cases for functions

.. _contributing_guide_code.where_to_start:

Forking
-------
You will need your own fork to work on the code. Go to the `flowrunner project page <https://github.com/prithvijitguha/flowrunner>`_ and hit the ``Fork`` button. You will
want to clone your fork to your machine

.. code-block:: bash

    git clone https://github.com/prithvijitguha/flowrunner.git flowrunner-username
    cd flowrunner-username
    git remote add upstream https://github.com/prithvijitguha/flowrunner.git

.. _contributing_guide_code.forking:

Creating a Branch
-----------------

.. code-block:: bash

    git branch shiny-new-feature
    git checkout shiny-new-feature

The above can be simplified to

.. code-block:: bash

    git checkout -b shiny-new-feature

.. _contributing_guide_code.creating_a_branch:

Commiting
----------

After you have made your changes. Let's say we have changed file ``modified_file``.

.. code-block:: bash

    git add modified_file

``pre-commit`` does a set of checks before you commit the code. Please ``pre-commit`` before ``commit``.

.. code-block:: bash

    pre-commit install

This will install a set of hooks and create a pre-commit environment.

.. code-block:: bash

    pre-commit run --files modified_file

Once your file passes the checks you can commit your changes.

.. code-block:: bash

    git commit -m "modified file modified_file"

.. _contributing_guide_code.commiting:

Pushing your code
-----------------

Once committed you can push your code.

.. code-block:: bash

    git push origin shiny-new-feature

.. _contributing_guide_code.pushing_your_code:


Create a Pull Request
---------------------
#. Navigate to your repository on GitHub
#. Click on the ``Pull Request`` button
#. You can then click on ``Commits`` and ``Files Changed`` to make sure everything looks
   okay one last time
#. Write a description of your changes in the ``Preview Discussion`` tab
#. Click ``Send Pull Request``.


.. _contributing_guide_code.create_a_pull_request:
