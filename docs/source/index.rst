Arya's API Framework
====================

This module is designed to be a base for the creation of clients that interact with RESTful web APIs.

**Features:**
   - Synchronous branch utilizing :resource:`requests <requests>`.
   - Asynchronous branch utilizing :resource:`aiohttp <aiohttp>`.
   - Integrated with :resource:`pydantic <pydantic>` for strict typing.

Installation
------------

To install the sync branch:

.. code-block::

   pip install arya-api-framework[sync]

To install the async branch:

.. code-block::

   pip install arya-api-framework[async]

Getting Started
---------------
.. toctree::

   quickstart
   logging

API Reference
--------------
.. toctree::
    :maxdepth: 2

    sync_framework
    async_framework
    models
    utils
    exceptions

Information
-----------
Check this out! :ref:`500`

.. toctree::
    :maxdepth: 2

    statuses

Stuck?
------
If you are struggling to find specific information, see these references:
    - `Search <search.html>`_
    - `Glossary <genindex.html>`_
