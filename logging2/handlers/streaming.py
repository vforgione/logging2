from io import TextIOWrapper
from sys import stderr, stdout
from typing import Optional

from logging2.handlers.abc import Handler
from logging2.levels import LogLevel


class StreamingHandler(Handler):
    """A generic ``Handler`` for writing log entries to a streaming endpoint such as STDOUT or STDERR.
    """

    def __init__(
            self,
            stream: TextIOWrapper,
            name: Optional[str]=None,
            level: Optional[LogLevel]=None
    ):
        """Initializes a new ``StreamingHandler``

        :param stream: the output stream object
        :param name: the name of the handler
        :param level: the minimum level of verbosity/priority of the messages this will log
        """
        self.stream: TextIOWrapper = stream
        super().__init__(name=name, level=level)

    def write(self, message: str, level: LogLevel) -> None:
        """Writes the full log entry to a configured stream

        :param message: the entire message to be written, full formatted
        :param level: the priority level of the message
        """
        if level >= self.min_level:
            self.stream.write(message)

    def _create_name(self) -> str:
        """Creates the name for the handler - called from ``__init__`` if a name is not given.

        :returns: the class name of the stream
        """
        return self.stream.__class__.__name__


class StdOutHandler(StreamingHandler):
    """An implementation of the ``StreamingHandler`` with ``sys.stdout`` preconfigured as the stream and
    named as ``stdout``
    """

    def __init__(
            self,
            name: Optional[str]='stdout',
            level: Optional[LogLevel]=None
    ):
        """Initializes a new ``StdOutHandler``

        :param name: the name of the handler
        :param level: the minimum level of verbosity/priority of the messages this will log
        """
        super().__init__(name=name, level=level, stream=stdout)


class StdErrHandler(StreamingHandler):
    """An implementation of the ``StreamingHandler`` with ``sys.stderr`` preconfigured as the stream and
    named as ``stderr``
    """

    def __init__(
            self,
            name: Optional[str]='stderr',
            level: Optional[LogLevel]=None
    ):
        """Initializes a new ``StdErrHandler``

        :param name: the name of the handler
        :param level: the minimum level of verbosity/priority of the messages this will log
        """
        super().__init__(name=name, level=level, stream=stderr)
