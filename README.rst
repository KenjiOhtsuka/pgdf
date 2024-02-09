====
pgdf
====

Tool built with **p**\ ython to summarize **g**\ it **d**\ if\ **f**.

**********
Motivation
**********

This tool can put diffs into Excel.

************
Installation
************

This tool is installed with pip:

.. code-block:: bash

    $ pip install pgdf

*****
Usage
*****

Go to the Git repository directory, then:

.. code-block:: bash

    $ pgdf 09c03f56 93496ef3
    $ pgdf 09c03f56 93496ef3 dir/path file/path
    $ pgdf feature/something origin/main

It generates an Excel file that contains summary of the differences.

************
Excel Format
************

The output excel file contains two sheets, :code:`Summary` and :code:`Diff`.

**Summary**

The summary sheet contains the summary of the differences.
It is same as the result of `git diff --stats` for the specified commits.

**Diff**

The diff sheet contains the differences of the markdown files.
It is something like `git diff` for the specified commits, but it also contains line numbers and commit short logs as follows.

.. table::

====
pgdf
====

Tool built with **p**\ython to summarize **g**\ it **d**\ if\ **f**.

**********
Motivation
**********

This tool can put diffs into Excel.

************
Installation
************

This tool is installed with pip:

.. code-block:: bash

    $ pip install pgdf

*****
Usage
*****

Go to the Git repository directory, then:

.. code-block:: bash

    $ pgdf 09c03f56 93496ef3
    $ pgdf 09c03f56 93496ef3 dir/path file/path
    $ pgdf origin/main feature/something

It generates an Excel file that contains summary of the differences.

************
Excel Format
************

The output excel file contains two sheets, :code:`Summary` and :code:`Diff`.

**Summary**

The summary sheet contains the summary of the differences.
It is same as the result of `git diff --stats` for the specified commits.

**Diff**

The diff sheet contains the differences of the markdown files.
It is something like `git diff` for the specified commits, but it also contains line numbers and commit short logs as follows.

+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
| Diff 29485862 4959956a                                                              |                     |                     |                                               |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
|                        |                |                     |                     |                     |                     |                                               |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
|                        |                |                     |                     |                     |                     | **diff --git a/file_a.txt b/file_a.txt**      |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
|                        |                |                     |                     |                     |                     | index 29485862..4959956a 100644               |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
|                        |                |                     |                     |                     |                     | --- a/file_a.txt                              |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
|                        |                |                     |                     |                     |                     | +++ b/file_a.txt                              |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
|                        |                |                     |                     |                     |                     | @@ -1,3 +1,3 @@                               |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
|                        |                |                     |                     |                     |                     |                                               |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
|                        |                |                     |                     |                  33 |                  33 | \ text 1                                      |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
|                        |                |                     |                     |                  34 |                  34 | \ text 2                                      |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
| 29485862               | User 1         | 2024-01-01 ...      | old comment         |                  35 |                     | \- old text 3                                 |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
| 4959956a               | User 2         | 2024-01-01 ...      | new comment         |                     |                  35 | \+ new text 3                                 |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
|                        |                |                     |                     |                  36 |                  36 |   text 4                                      |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+
|                        |                |                     |                     |                  37 |                  37 |   text 5                                      |
+------------------------+----------------+---------------------+---------------------+---------------------+---------------------+-----------------------------------------------+


************
PyPI package
************

https://pypi.org/project/pgdf/

