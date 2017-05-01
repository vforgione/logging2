==========
 logging2
==========

A More Pythonic Logging System; *or,* You Deserve Better Than log4j

.. image:: https://travis-ci.org/vforgione/logging2.svg?branch=master
   :target: https://travis-ci.org/vforgione/logging2
.. image:: https://coveralls.io/repos/github/vforgione/logging2/badge.svg?branch=master
   :target: https://coveralls.io/github/vforgione/logging2?branch=master
.. image:: https://readthedocs.org/projects/logging2/badge/?version=latest
   :target: http://logging2.readthedocs.io/en/latest/?badge=latest

-------------------------------
 The Basic Contract of Logging
-------------------------------

Logging should be simple and intuitive.

For most use cases, you want to quickly instantiate a logger and dump some text
to a stream. You would expect a common workflow based on a minimum level of
verbosity in the log entries and for those entries to be formatted in some
fashion that is both human readable and machine parseable. There should also be
a set of common metadata that can be used to provide context to the entry.

That context should also be easily extended to suit everyone's use cases.
Additionally, the values passed to that context should be pliable - users should
have the option to override those values as they deem necessary.

Common meta information should conform to as widely adopted standards as
possible - i.e. ISO 8601 timestamps and full unicode supported messages.

As stated foremost, the interface to this system should be simple and
intuitive. This means the complexity of the system should be minimized,
configuration should have sane defaults and the supporting library should
be packed with expressive documentation.

Implementation of the Contract
------------------------------

The user should only be concerned with three components:

- Verbosity (``LogLevel``)
- Message Producers (``Handler``)
- Message Creation (``Logger``)

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

---------
 Caveats
---------

**This logging utility is designed for Python 3.6 and better.** It will not be
backported to support any earlier versions of Python.
