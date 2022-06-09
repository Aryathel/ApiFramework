Arya's API Framework
====================

.. image:: https://img.shields.io/pypi/v/arya_api_framework.svg
   :target: https://pypi.python.org/project/arya-api-framework/
   :alt: PyPI version info

.. image:: https://img.shields.io/pypi/pyversions/arya_api_framework.svg
   :target: https://pypi.python.org/project/arya-api-framework/
   :alt: PyPI supported Python versions

This is a simple package that is meant to be a
`Pydantic <https://pydantic-docs.helpmanual.io/>` implementation
for a basic RESTful API interaction client. This includes both sync and async usages.

Installation
------------
Synchronous implementation - if you aren't sure, you probably want this:

.. code-block:: sh

    python -m pip install arya-api-framework[sync]

Asynchronous implementation:

.. code-block:: sh

    python -m pip install arya-api-framework[async]

----

Note
----
This may be documented properly in the future, but I don't really see a reason for that
right now, given that I am only creating for specific usages.