==========
 logging2
==========

A More Pythonic Logging System *or* You Deserve Better Than ``log4j``

----------
 Contents
----------

.. toctree::
   :maxdepth: 2

   levels_and_workflow
   handlers
   loggers


--------------
 Installation
--------------

``logging2`` is available through PyPI, and thus can be installed via pip::

  $ pip install logging2


------------
 Quickstart
------------

Logging should be simple and intuitive. With that in mind, the easiest way to get up and running is
to instantiate a ``Logger`` and start producing entries::

  >>> from logging2 import Logger

  >>> logger = Logger('app')
  >>> logger.info('Hello, world!')
  2017-04-29T17:08:23.156795+00:00 INFO app: Hello, world!

The default logger will dump all log entries to STDOUT with a minimum verbosity of ``info``.

There are numerous configurations, all with simple and easy to rationalize behavior:

- log entry verbosity
- log producers (handlers)
- intuitive interface to creating log entries (loggers)

``Logger`` s have a handful of ways of creating log entries via:

- ``debug`` for the most verbose level of messages
- ``info`` for typical informational messages
- ``warning`` for calling user attention to a potentially hazardous conditions
- ``error`` for altering users to captured and recovered from error conditions
- ``exception`` for capturing exception tracebacks in the log

The mechanism for producing the log entries to the output streams is via ``Handler`` s. Handlers
are broken into three groups:

- ``streaming`` for common IO messaging (typically STDOUT and STDERR)
- ``files`` for file system based IO
- ``sockets`` for network based messaging

All of which are found in the ``logging2.handlers`` package.
