from typing import Union

from logging2.utils import Singleton


class _LogRegister(metaclass=Singleton):
    """A Singleton object for storing ``Logger``s. Loggers are essentially Borgs, but rather than a traditional Borg
    where every instance shares state, loggers share state by name. That is, if a logger is named ``request_logger``
    and another is named ``response_logger``, they don't necessarily need to share the same state information -- just
    other instances with the same name do.
    """

    def __init__(self):
        self._loggers = {}

    def __contains__(self, item) -> bool:
        return self._loggers.__contains__(item)

    def register_logger(self, logger: 'Logger') -> None:
        """Registers a named ``Logger``.

        :param logger: the logger to be considered for registration
        """
        name = logger.name
        if name not in self._loggers:
            self._loggers[name] = logger

    def get_logger(self, name) -> Union['Logger', None]:
        """Gets a ``Logger`` from the register if it exists.

        :param name: the name of the logger
        :returns: the registered logger
        """
        return self._loggers.get(name)


LogRegister = _LogRegister()


# finish imports - bubble most common import to `logging2` namespace

from logging2.handlers.files import FileHandler
from logging2.handlers.streaming import StdErrHandler, StdOutHandler
from logging2.levels import LogLevel
from logging2.loggers import Logger
