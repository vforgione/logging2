.. loggers:

=========
 Loggers
=========

Logger is the main interface to the library. It has the responsibility of taking user messages and
interpolating them, and other context values, with a log entry template to create a message that is
then passed to the attached handlers.

----------------
 Default Logger
----------------

The default logger will lazily create a handler that writes to STDOUT with a minimum verbosity of
INFO. Its output template is a simple ``{timestamp} {level} {name}: {message}``. For example::

   >>> from logging2 import Logger
   >>> logger = Logger('app')
   >>> logger.info('Hello, world!')
   2017-04-29T17:08:23.156795+00:00 INFO app: Hello, world!

--------------------
 Basic Logger Usage
--------------------

Of course that's not all to using the logger interface. There are numerous ways of configuring a
logger. You can set verbosity level, add one or more handlers (thus disabling the default STDOUT
handler), set the timestamp's timezone (timestamps are ISO 8601 formatted and default to UTC) and
provide a custom template.

**Setting Verbosity for the Default Handler**

If you only need the default handler but want to change its verbosity, all you need to do is set
the ``level`` parameter of the logger on instantiation::

   >>> from logging2 import Logger, LegLevel
   >>> logger = Logger('app', level=LogLevel.error)
   >>> logger.info('Hello, world!')  # nothing
   >>> logger.error('Hello, world!')
   2017-04-29T17:08:23.156795+00:00 ERROR app: Hello, world!

**Adding Handlers**

Handlers can be set up a couple different ways:

- there's a default StdOutHandler lazily created when a logging method is called if no handlers are present
- there's a ``handler`` parameter to set a different default handler for the logger
- there's a ``handlers`` (note the *s*) to pass a list of handlers to the logger
- you can use the ``add_handler`` method of the logger as well at any time

Using the ``handler`` kwarg on init::

   >>> from logging2 import Logger, FileHandler
   >>> fh_handler = FileHandler(file_path='/var/log/app.log')
   >>> logger = Logger('app', handler=fh_handler)

Using the ``handlers`` kwarg on init::

   >>> from logging2 import Logger, FileHandler, StdOutHandler, LogLevel
   >>> fh_handler = FileHandler(file_path='/var/log/app.log')
   >>> stdout = StdOutHandler(level=LogLevel.debug)
   >>> logger = Logger('app', handlers=[fh_handler, stdout])

-----------------------
 Advanced Logger Usage
-----------------------

Beyond all of this there's some advanced work you can do with loggers as well. You can inject context
into the message at any time: either during initialization or at log time.

**Using the ``additional_context`` Kwarg**

There's another keyword available for the logger's init - ``additional_context``. It take a dictionary
of values to inject into the context of the log entry that will override any system default. You can
also use it to provide context values for ony non-default template keys (such as injecting request ids
into the log entry).

Let's say we have a machine id that we want logged. The id is pulled from an environment variable
that uniquely identifies the server (pretending we have a distributed application and are using some
sort of networked log collector)::

   >>> import os
   >>> from logging import Logger
   >>> from logging.handlers import UdpHandler

   >>> machine_id = os.environ.get('MACHINE_ID')
   >>> template = '{timestamp} {machine} {level}: {message}'
   >>> logger = Logger(name='app', template=template, additional_context={'machine': machine_id})
   >>> handler = UdpHandler(host='10.2.1.99', port=5000)
   >>> logger.add_handler(handler)

Now when we send logs, they will include this machine's identifier.

But we don't always have static information that we want to inject - sometimes we need to be able to
get information on the fly such as a request id. Easy enough, the value parts of the dictionary can
also be functions (the system will check if the value is static or callable). Let's pretend we have a
flask app with a ``request_id`` being set on the global ``g`` object::

   >>> def get_request_id():
   ...      return g.request_id
   ...
   >>> template = '{timestamp} {req_id} {level}: {message}'
   >>> logger = Logger(name='app', template=template, additional_context={'req_id': get_request_id})

**Overloading the Logging Methods**

There's one last way to provide any final overload to a template key - providing the kwarg directly
in the logging calls (``debug``, ``info``, etc.)::

   >>> logger.info('Hello, world!', timestamp='whenever')
   whenever INFO app: Hello, world!

-----
 API
-----

.. autoclass:: logging2.loggers.Logger
   :special-members: __init__
   :members:
   :member-order: bysource
