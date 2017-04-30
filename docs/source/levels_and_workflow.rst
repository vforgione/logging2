.. _levels_and_workflow:

=====================
 Levels and Workflow
=====================

The most basic component of logging is the log entry verbosity (or priority) and how that informs
the overall workflow. There are 5 levels of verbosity that are used in this library:

- debug
- info
- warning
- error
- exception

Each of these has a graduating level of priority in the system: ``debug`` being the lowest and most
verbose; ``exception`` being the highest and most restrictive.

``Handler`` s are configured to have a *minimum level of verbosity*. That is, if a handler is configured
to only produce log entries with a minimum level of ``info``, all messages passed to it with a level
of ``debug`` will not be recorded; anything else greater than or equal to the set minimum level
will be recorded. For example::

  >>> from logging2.handlers import StdOutHandler
  >>> from logging2.levels import LogLevel

  >>> handler = StdOutHandler(level=LogLevel.debug)  # sets handler to log everything
  >>> handler.write('Hello\n', level=LogLevel.debug)
  Hello
  >>> handler.write('Hello\n', level=LogLevel.info)
  Hello

  >>> handler = StdOutHandler(level=LogLevel.error)  # sets handler to log only errors and exceptions
  >>> handler.write('Hello\n', level=LogLevel.debug)  # skipped
  >>> handler.write('Hello\n', level=LogLevel.info)  # skipped
  >>> handler.write('Hello\n', level=LogLevel.error)
  Hello

This workflow is helpful in that ``Logger`` s can have multiple handlers attached to them, each with
a distinct level of verbosity::

  # test.py
  from logging2 import Logger, LogLevel, StdOutHandler, StdErrHandler

  stdout = StdOutHandler()
  stderr = StdErrHandler(level=LogLevel.error)
  logger = Logger('test', handlers=[stdout, stderr])

  logger.debug('this is a debug message')
  logger.info('this is an info message')
  logger.warning('this is a warning message')
  logger.error('this is an error message')

  try:
      1 / 0
  except ZeroDivisionError:
      logger.exception("world's best breakpoint")

Which if you ran directly in the terminal would look like::

  2017-04-29T17:36:31.560942+00:00 INFO test: this is an info message
  2017-04-29T17:36:31.561007+00:00 WARNING test: this is a warning message
  2017-04-29T17:36:31.561041+00:00 ERROR test: this is an error message
  2017-04-29T17:36:31.561041+00:00 ERROR test: this is an error message
  2017-04-29T17:36:31.561070+00:00 EXCEPTION test: world's best breakpoint
  Traceback (most recent call last):
    File "test.py", line 13, in <module>
      1 / 0
  ZeroDivisionError: division by zero

  2017-04-29T17:36:31.561070+00:00 EXCEPTION test: world's best breakpoint
  Traceback (most recent call last):
    File "test.py", line 13, in <module>
      1 / 0
  ZeroDivisionError: division by zero

A better approach would be a general log and an error log::

  $ python test.py > test.log 2>error.log

  # test.log
  2017-04-29T17:37:51.764118+00:00 INFO test: this is an info message
  2017-04-29T17:37:51.764141+00:00 WARNING test: this is a warning message
  2017-04-29T17:37:51.764157+00:00 ERROR test: this is an error message
  2017-04-29T17:37:51.764176+00:00 EXCEPTION test: world's best breakpoint
  Traceback (most recent call last):
    File "test.py", line 13, in <module>
      1 / 0
  ZeroDivisionError: division by zero

  # error.log
  2017-04-29T17:37:51.764157+00:00 ERROR test: this is an error message
  2017-04-29T17:37:51.764176+00:00 EXCEPTION test: world's best breakpoint
  Traceback (most recent call last):
    File "test.py", line 13, in <module>
      1 / 0
  ZeroDivisionError: division by zero

The last thing to note here, obviously, is that each ``LogLevel`` value has a corresponding method
in ``Logger`` that sets the priority of the message passed to the handlers.
