from typing import Optional

from logging2.levels import LogLevel


class Handler:
    """``Handler`` is the interface that all handlers must implement. It defines the API for handlers - namely the
    ``write`` method of each that produces the log entries.
    """

    DEFAULT_LOG_LEVEL: LogLevel = LogLevel.info

    def __init__(
            self,
            name: Optional[str]=None,
            level: Optional[LogLevel]=None
    ):
        """Instantiates a new ``Handler``

        :param name: the name of the handler
        :param level: the minimum level of verbosity/priority of the messages this will log
        """
        self.name = name or self._create_name()
        self.min_level: LogLevel = level or self.DEFAULT_LOG_LEVEL

    def write(self, message: str, level: LogLevel) -> None:
        """Writes the full log entry to a configured stream

        :param message: the entire message to be written, full formatted
        :param level: the priority level of the message
        """
        raise NotImplementedError  # pragma: no cover

    def _create_name(self) -> str:
        """Creates the name for the handler - called from ``__init__`` if a name is not given.

        :returns: an appropriate name for the handler
        """
        raise NotImplementedError  # pragma: no cover
