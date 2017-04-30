import inspect
import os
import re
import sys
import traceback
from datetime import datetime, tzinfo
from datetime import timezone as _tz
from typing import Callable, Dict, Iterable, List, Optional, Set, Union

from logging2 import LogRegister
from logging2.handlers.abc import Handler
from logging2.handlers.streaming import StdOutHandler
from logging2.levels import LogLevel


class Logger:
    """`A ``Logger`` is the main interface to passing user messages and assembling metadata for log entries.
    """

    TEMPLATE_KEYS_REGEX = re.compile('\{(?P<key>\w+)\}')
    BASE_TEMPLATE_KEYS = {'timestamp', 'level', 'name', 'message', 'source', 'line', 'function', 'process'}

    DEFAULT_TEMPLATE: str = '{timestamp} {level} {name}: {message}'
    DEFAULT_TIMEZONE: tzinfo = _tz.utc
    DEFAULT_HANDLER_CLASS: type = StdOutHandler
    DEFAULT_LOG_LEVEL: LogLevel = LogLevel.info

    def __init__(
            self,
            name: str,
            template: Optional[str]=None,
            ensure_new_line: Optional[bool]=True,
            timezone: Optional[tzinfo]=None,
            additional_context: Optional[Dict[str, Union[object, Callable]]]=None,
            handler: Optional[Handler]=None,
            handlers: Optional[Iterable[Handler]]=None,
            level: Optional[LogLevel]=None
    ):
        """Instantiates a new ``Logger``

        :param name: the name of the logger
        :param template: the template used to create log entries
        :param ensure_new_line: should the log entry always end with a new line character
        :param timezone: timezone for ISO 8601 timestamp formatting
        :param additional_context: key-value pairs used to provide context to template interpolation
        :param handler: a handler to be registered to this logger
        :param handlers: a group of handlers to be registered to this logger
        :param level: sets the log level for the default handler
        """
        if name not in LogRegister:
            self.name: str = name
            self.ensure_new_line: bool = ensure_new_line
            self.timezone: tzinfo = timezone or self.DEFAULT_TIMEZONE
            self.additional_context: Optional[Dict[str, Union[object, Callable]]] = additional_context or {}

            self._level: LogLevel = level
            self._template: str = None
            self._keys: Set[str] = None
            self._setup_template(template=template or self.DEFAULT_TEMPLATE)

            self._handlers: Dict[str, Handler] = {}
            if handler:
                self.add_handler(handler)
            if handlers:
                for handler in handlers:
                    self.add_handler(handler)

            LogRegister.register_logger(self)

        else:
            registered = LogRegister.get_logger(name=name)
            self.__dict__ = registered.__dict__

    @property
    def template(self) -> str:
        return self._template

    @template.setter
    def template(self, new_template: str) -> None:
        self._setup_template(template=new_template)

    @property
    def keys(self) -> Set[str]:
        return self._keys

    @property
    def handlers(self) -> List[Handler]:
        return [handler for handler in self._handlers.values()]

    def add_handler(self, handler: Handler) -> None:
        """Adds a new ``Handler`` to the list of handlers.

        :param handler: the new handler
        """
        name = handler.name
        if name not in self._handlers:
            self._handlers[name] = handler

    def remove_handler(self, name: str) -> None:
        """Removes a ``Handler`` from the list of handlers.

        :param name: the name of the handler to be removed
        """
        if name in self._handlers:
            del self._handlers[name]

    def debug(self, message: str, **context) -> None:
        """Calls each registered ``Handler``'s ``write`` method to produce a debug log entry.

        :param message: the user message to be written
        :param context: additional key-value pairs to override template context during interpolation
        """
        self._log(message=message, level=LogLevel.debug, **context)

    def info(self, message: str, **context) -> None:
        """Calls each registered ``Handler``'s ``write`` method to produce an info log entry.

        :param message: the user message to be written
        :param context: additional key-value pairs to override template context during interpolation
        """
        self._log(message=message, level=LogLevel.info, **context)

    def warning(self, message: str, **context) -> None:
        """Calls each registered ``Handler``'s ``write`` method to produce a warning log entry.

        :param message: the user message to be written
        :param context: additional key-value pairs to override template context during interpolation
        """
        self._log(message=message, level=LogLevel.warning, **context)

    def error(self, message: str, **context) -> None:
        """Calls each registered ``Handler``'s ``write`` method to produce an error log entry.

        :param message: the user message to be written
        :param context: additional key-value pairs to override template context during interpolation
        """
        self._log(message=message, level=LogLevel.error, **context)

    def exception(self, message: str, **context) -> None:
        """Calls each registered ``Handler``'s ``write`` method to produce an exception log entry.

        :param message: the user message to be written
        :param context: additional key-value pairs to override template context during interpolation
        """
        self._log(
            message=message, level=LogLevel.exception,
            capture_error=True, **context)

    def _log(
            self,
            message: str,
            level: LogLevel,
            capture_error: bool=False,
            **context) -> None:
        """Performs all information retrieval, does template interpolation and calls the handlers to write the message.

        :param message: the ``{message}`` portion of the log entry
        :param level: the verbosity/priority level of the message
        :param capture_error: should the calling frame be inspected for any errors
        :param context: key-value pairs to override template context during interpolation
        """
        if not len(self._handlers):
            default_handler = self.DEFAULT_HANDLER_CLASS(level=self._level or self.DEFAULT_LOG_LEVEL)
            self.add_handler(default_handler)

        if self.ensure_new_line and not message.endswith('\n'):
            message = f'{message}\n'

        params = {'message': message, 'level': level, 'name': self.name}

        if 'timestamp' in self.keys:
            params['timestamp'] = self._get_timestamp()

        if {'source', 'line', 'function', 'process'} & self.keys:
            exec_info = self._get_exec_info()
            params.update(exec_info)

        if capture_error:
            tb = traceback.format_exc()
            params['message'] = '{}{}\n'.format(message, tb)

        for key, value in self.additional_context.items():
            if inspect.isfunction(value):
                params[key] = value()
            else:
                params[key] = value

        for key, value in context.items():
            if inspect.isfunction(value):
                params[key] = value()
            else:
                params[key] = value

        output = self.template.format(**params)
        for handler in self._handlers.values():
            handler.write(output, level=level)

    def _setup_template(self, template: str) -> None:
        """Sets up the ``_template`` and ``_keys`` attributes based on the input template.

        :param template: the template to be parsed
        """
        keys = self.TEMPLATE_KEYS_REGEX.findall(template)
        if not keys:
            raise ValueError(f'No keys found in template `{template}`')
        self._template = template
        self._keys = set(keys)

    def _get_timestamp(self) -> str:
        """Gets the ISO 8601 formatted timestamp for the current time.

        :returns: the ISO 8601 formatted timestamp for the current time
        """
        return datetime.now(self.timezone).isoformat()

    @staticmethod
    def _get_exec_info() -> dict:
        """Gets the execution information of the calling stack.

        :returns: a dictionary to be used for interpolating execution information into log entries
        """
        frame = sys._getframe(3)
        fname, line, func, _, __ = inspect.getframeinfo(frame)
        if func == '<module>':
            func = '__main__'  # pragma: no cover
        return {
            'source': fname,
            'function': func,
            'line': line,
            'process': os.getpid(),
        }
