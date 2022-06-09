.. Arya's API Framework documentation master file, created by
   sphinx-quickstart on Tue Jun  7 22:38:32 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

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
   utils
   models