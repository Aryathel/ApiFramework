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
              - |license| |language| |requires|

    .. |docs| rtfd-shield::
        :class: shield
        :project: apiframework
        :alt: Documentation Build Status

    .. |requires| image:: https://dependency-dash.herokuapp.com/github/Aryathel/ApiFramework/badge.svg
        :class: shield
        :target: https://dependency-dash.herokuapp.com/github/Aryathel/APIFramework/
        :alt: Requirements Status

    .. |codefactor| codefactor-shield::
        :alt: CodeFactor Grade
        :class: shield

    .. |pypi-version| pypi-shield::
        :class: shield
        :project: arya-api-framework
        :version:
        :alt: PyPI - Package Version

    .. |supported-versions| pypi-shield::
        :class: shield
        :project: arya-api-framework
        :py-versions:
        :alt: PyPI - Supported Python Versions

    .. |supported-implementations| pypi-shield::
        :class: shield
        :project: arya-api-framework
        :implementations:
        :alt: PyPI - Supported Implementations

    .. |wheel| pypi-shield::
        :class: shield
        :project: arya-api-framework
        :wheel:
        :alt: PyPI - Wheel

    .. |license| github-shield::
        :class: shield
        :license:
        :alt: License

    .. |language| github-shield::
        :class: shield
        :top-language:
        :alt: GitHub top language

    .. |commits-latest| github-shield::
        :class: shield
        :last-commit:
        :branch: main
        :alt: GitHub last commit

    .. |maintained| maintained-shield:: 2022
        :class: shield
        :alt: Maintenance

    .. |pypi-downloads| pypi-shield::
        :class: shield
        :project: arya-api-framework
        :downloads: month
        :alt: PyPI - Downloads

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
Check this out! :ref:`500`

.. toctree::
    :maxdepth: 2

    statuses

Stuck?
------
If you are struggling to find specific information, see these references:
    - `Search <search.html>`_
    - `Glossary <genindex.html>`_
