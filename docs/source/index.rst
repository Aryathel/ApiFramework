Arya's API Framework
====================

.. only:: html

    .. list-table::
        :stub-columns: 1
        :widths: 10 90

        * - Docs
          - |docs|
        * - PyPI
          - |pypi-version| |supported-versions| |supported-implementations| |wheel|
        * - Activity
          - |commits-latest| |maintained| |pypi-downloads|
        * - QA
          - |codefactor|
        * - Other
          - |license| |language|

.. |docs| image:: https://img.shields.io/readthedocs/apiframework/latest?logo=read-the-docs&color=purple&logoColor=white
    :class: shield
    :target: https://apiframework.readthedocs.io/en/latest/
    :alt: RTFD - Docs Build Status

.. |pypi-version| image:: https://img.shields.io/pypi/v/arya-api-framework?color=purple
    :class: shield
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/arya-api-framework?logo=python&logoColor=white&color=purple
    :class: shield
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/arya-api-framework?color=purple
    :class: shield
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/arya-api-framework?color=purple
    :class: shield
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Wheel

.. |commits-latest| image:: https://img.shields.io/github/last-commit/Aryathel/ApiFramework/main?color=purple
    :class: shield
    :target: https://github.com/Aryathel/APIFramework
    :alt: Github - Last Commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022?color=purple
    :class: shield
    :target: https://github.com/Aryathel/APIFramework/commit/main
    :alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/arya-api-framework?color=purple
    :class: shield
    :target: https://pypistats.org/packages/arya-api-framework
    :alt: PyPI - Downloads

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/Aryathel/ApiFramework?logo=codefactor&color=purple&logoColor=white
    :class: shield
    :target: https://www.codefactor.io/repository/github/Aryathel/ApiFramework
    :alt: CodeFactor - Grade

.. |license| image:: https://img.shields.io/github/license/Aryathel/ApiFramework?color=purple
    :class: shield
    :target: https://github.com/Aryathel/ApiFramework/blob/main/LICENSE
    :alt: GitHub - License

.. |language| image:: https://img.shields.io/github/languages/top/Aryathel/ApiFramework?color=purple
    :class: shield
    :target: https://github.com/Aryathel/ApiFramework
    :alt: GitHub - Top Language

This module is designed to be a base for the creation of clients that interact with RESTful web APIs.

**Features:**
   - Synchronous branch utilizing :resource:`requests <requests>`.
   - Asynchronous branch utilizing :resource:`aiohttp <aiohttp>`.
   - Integrated with :resource:`pydantic <pydantic>` for strict typing.

Installation
------------

To install the sync branch:

.. code-block:: sh

   pip install arya-api-framework[sync]

To install the async branch:

.. code-block:: sh

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
Here lies a bunch of random information related to the project at least a little bit.

.. toctree::
    :maxdepth: 2

    statuses

Glossary
--------
If you are struggling to find specific information, see these references:

    * `Search <search.html>`_
    * `Glossary <genindex.html>`_
