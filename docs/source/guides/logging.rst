.. _logging_setup:

Logging
=======
This API Framework logs errors via the :mod:`logging` module. By default, no warnings or status updates from
the library will be shown. To run on logging for your API client, you can simply enable it at the top of your
primary file like so:

.. code-block:: python

    import logging
    logging.basicConfig(level = logging.INFO)

The specification of the ``level`` argument decides what tier of events the :mod:`logging` modules will output.
These can be ``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO``, and ``DEBUG``. By default, the logging level is set to
`WARNING``.

It is also possible to implement custom formatting of log outputs, as well as sending logs to a file.
For example, to send logs to a file called ``api.log``. To do this, you will have to update the loggers
for the clients included in the API Framework:

.. code-block:: python

    import arya_api_framework
    import logging

    # Retrieve the logger for the specific client you are using.
    # (Ideally you only need to use one or the other.)
    sync_logger = logging.getLogger('arya_api_framework.Sync')
    async_logger = logging.getLogger('arya_api_framework.Async')

    # Set the logging level of the logger.
    sync_logger.setLevel(logging.INFO)
    async_logger.setLevel(logging.DEBUG)

    # Create a handler to direct log posts to a file.
    handler = logging.FileHandler(filename='api.log', encoding='utf-8', mode='w')

    # Create a formatter to handle formatting a log entry.
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')

    # Set the loggers to use the file handler and log formatter.
    handler.setFormatter(formatter)
    sync_logger.addHandler(handler)
    async_logger.addHandler(handler)

.. note::

    It is recommended that you enable logging at least to the ``Info`` level, as information on the status of each
    API request will be shown there. To avoid this clogging your stdout, you might also want to log events to a file.

For more information about how to handle logging, check out the :mod:`logging` module directly.
