from logging2.utils import Singleton


class _LogRegister(metaclass=Singleton):
    def __init__(self):
        self._loggers = {}

    def __contains__(self, item):
        return self._loggers.__contains__(item)

    def register_logger(self, logger):
        name = logger.name
        if name not in self._loggers:
            self._loggers[name] = logger

    def get_logger(self, name):
        return self._loggers.get(name)


LogRegister = _LogRegister()


# finish imports

from logging2.handlers.files import FileHandler
from logging2.handlers.streaming import StdErrHandler, StdOutHandler
from logging2.levels import LogLevel
from logging2.loggers import Logger
