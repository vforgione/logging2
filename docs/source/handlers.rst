.. handlers:

==========
 Handlers
==========

``Handler`` s are what push the finalized log entries to the output streams. They have a common
interface with a default required ``name`` and a ``write`` method.


-----------
 Streaming
-----------

Streaming handlers write to basic IO streams, such as STDOUT and STDERR. There is one basic
``StreamingHandler`` and two convenience handlers that inherit from that: ``StdOutHandler`` and
``StdErrHandler``.

.. autoclass:: logging2.handlers.streaming.StreamingHandler
   :special-members: __init__
   :members:
   :private-members:

.. autoclass:: logging2.handlers.streaming.StdOutHandler
   :special-members: __init__
   :members:
   :private-members:

.. autoclass:: logging2.handlers.streaming.StdErrHandler
   :special-members: __init__
   :members:
   :private-members:


-------
 Files
-------

There is one type of file handler: ``FileHandler``. This module does not provide handlers for rotating
log files. The rationale behind that is that all \*NIX systems have software specifically designed to
do that, and it's much faster and reliable. Let's separate concerns here: this logging software is
meant to be both Pythonic and fast. There's nothing Pythonic or fast about reinventing the wheel. A
great utility for log rotation is ``logrotate``, which is available for Debian, Red Hat, and BSD systems.

Linux Manpage: https://linux.die.net/man/8/logrotate

FreeBSD Manpage: https://www.freebsd.org/cgi/man.cgi?query=logrotate&manpath=SuSE+Linux/i386+11.3

.. autoclass:: logging2.handlers.files.FileHandler
   :special-members: __init__
   :members:
   :private-members:


---------
 Sockets
---------

Socket handlers write messages to socket connections - these can be anything from internet wide
network connections to local filesystem UNIX sockets.

There is one base ``SocketHandler`` type provided by the module. It can be used in a number of
ways to setup any sort of socket based logging. There are several other convenience handlers as well
that have presets for socket families and types.

.. autoclass:: logging2.handlers.sockets.SocketHandler
   :special-members: __init__
   :members:
   :private-members:

.. autoclass:: logging2.handlers.sockets.TcpHandler
   :special-members: __init__
   :members:
   :private-members:

.. autoclass:: logging2.handlers.sockets.TcpIPv6Handler
   :special-members: __init__
   :members:
   :private-members:

.. autoclass:: logging2.handlers.sockets.UdpHandler
   :special-members: __init__
   :members:
   :private-members:

.. autoclass:: logging2.handlers.sockets.UdpIPv6Handler
   :special-members: __init__
   :members:
   :private-members:

.. autoclass:: logging2.handlers.sockets.UnixSocketHandler
   :special-members: __init__
   :members:
   :private-members:

.. autoclass:: logging2.handlers.sockets.SyslogHandler
   :special-members: __init__
   :members:
   :private-members:
