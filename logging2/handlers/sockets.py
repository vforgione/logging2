import socket
import syslog
from typing import Optional

from logging2.handlers.abc import Handler
from logging2.levels import LogLevel


class SocketHandler(Handler):
    """A generic ``Handler`` for writing messages to sockets.
    """

    def __init__(
            self,
            name: Optional[str]=None,
            level: Optional[LogLevel]=None,
            **kwargs
    ):
        """Instantiates a new ``SocketHandler``

        :param name: the name of the handler
        :param level: the minimum verbosity level to write log entries
        :keyword host: the host portion of the connection -- this can be an FQDN, IP or a local UNIX socket node name
        :keyword port: the port number to connect on
        :keyword encoding: the message encoding
        :keyword family: the socket family -- for example AF_UNIX or AF_INET
        :keyword type: the socket type -- for example SOCK_STREAM or SOCK_DGRAM
        """
        self.host: str = kwargs.get('host')
        self.port: str = kwargs.get('port')
        self.encoding: str = kwargs.get('encoding', 'utf8')
        self.family: int = kwargs.get('family')
        self.type: int = kwargs.get('type')

        super().__init__(name=name, level=level)

        if self.port is not None and self.type != socket.SOCK_DGRAM:
            sock = socket.create_connection((self.host, self.port))
        else:
            if self.port:
                address = (self.host, self.port)
            else:
                address = (self.host)
            if self.family and self.type:
                sock = socket.socket(self.family, self.type)
            elif self.type:  # pragma: no cover
                sock = socket.socket(socket.AF_UNIX, self.type)
                self.family = socket.AF_UNIX
            else:  # pragma: no cover
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                self.family = socket.AF_UNIX
                self.type = socket.SOCK_DGRAM
            sock.connect(address)
        self.socket: socket.socket = sock

    def write(self, message: str, level: LogLevel) -> None:
        """Writes the full log entry to the configured socket

        :param message: the entire message to be written, full formatted
        :param level: the priority level of the message
        """
        if level >= self.min_level:
            self.socket.sendall(bytes(message, self.encoding))

    def _create_name(self) -> str:
        """Creates the name for the handler - called from ``__init__`` if a name is not given.

        :returns: a template of `({protocol} )?{host}(:{port})?`
        """
        if self.port:
            port = ':{}'.format(self.port)
        else:
            port = ''

        if self.family == socket.AF_UNIX:
            stype = 'UNIX'
        elif self.type == socket.SOCK_STREAM:
            stype = 'TCP'
        elif self.type == socket.SOCK_DGRAM:
            stype = 'UDP'
        else:
            stype = None  # pragma: no cover

        if stype:
            host = ' {}'.format(self.host)
        else:
            host = self.host  # pragma: no cover

        return '{}{}{}'.format(stype, host, port)


class TcpHandler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send TCP messages over a streaming socket via IPv4.
    """

    def __init__(
            self,
            host: str,
            port: int,
            encoding: Optional[str]='utf8',
            name: Optional[str]=None,
            level: Optional[LogLevel]=None
    ):
        """Instantiates a new ``TcpHandler``

        :param host: the server's hostname -- an FQDN, an IP address, anything that can be resolved
        :param port: the server's port
        :param encoding: the message encoding
        :param name: the name of the handler
        :param level: the minimum verbosity level to write log entries
        """
        super().__init__(
            name=name, level=level, host=host, port=port, family=socket.AF_INET,
            type=socket.SOCK_STREAM, encoding=encoding)


class TcpIPv6Handler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send TCP messages over a streaming socket via IPv6.
    """

    def __init__(
            self,
            host: str,
            port: int,
            encoding: Optional[str]='utf8',
            name: Optional[str]=None,
            level: Optional[LogLevel]=None
    ):
        """Instantiates a new ``TcpIPv6Handler``

        :param host: the server's hostname -- an FQDN, an IP address, anything that can be resolved
        :param port: the server's port
        :param encoding: the message encoding
        :param name: the name of the handler
        :param level: the minimum verbosity level to write log entries
        """
        super().__init__(
            name=name, level=level, host=host, port=port,
            family=socket.AF_INET6, type=socket.SOCK_STREAM, encoding=encoding)


class UdpHandler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send UDP messages via IPv4.
    """

    def __init__(
            self,
            host: str,
            port: int,
            encoding: Optional[str]='utf8',
            name: Optional[str]=None,
            level: Optional[LogLevel]=None
    ):
        """Instantiates a new ``UdpHandler``

        :param host: the server's hostname -- an FQDN, an IP address, anything that can be resolved
        :param port: the server's port
        :param encoding: the message encoding
        :param name: the name of the handler
        :param level: the minimum verbosity level to write log entries
        """
        super().__init__(
            name=name, level=level, host=host, port=port, family=socket.AF_INET,
            type=socket.SOCK_DGRAM, encoding=encoding)


class UdpIPv6Handler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send UDP messages via IPv6.
    """

    def __init__(
            self,
            host: str,
            port: int,
            encoding: Optional[str]='utf8',
            name: Optional[str]=None,
            level: Optional[LogLevel]=None
    ):
        """Instantiates a new ``UdpIPv6Handler``

        :param host: the server's hostname -- an FQDN, an IP address, anything that can be resolved
        :param port: the server's port
        :param encoding: the message encoding
        :param name: the name of the handler
        :param level: the minimum verbosity level to write log entries
        """
        super().__init__(
            name=name, level=level, host=host, port=port,
            family=socket.AF_INET6, type=socket.SOCK_DGRAM, encoding=encoding)


class UnixSocketHandler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send messages as datagrams to a local UNIX socket.
    """

    def __init__(
            self,
            node: str,
            encoding: Optional[str]='utf8',
            name: Optional[str]=None,
            level: Optional[LogLevel]=None
    ):
        """Instantiates a new ``UnixHandler``

        :param node: the path to the socket node on the system
        :param encoding: the message encoding
        :param name: the name of the handler
        :param level: the minimum verbosity level to write log entries
        """
        super().__init__(
            name=name, level=level, host=node, family=socket.AF_UNIX,
            type=socket.SOCK_DGRAM, encoding=encoding)


class SyslogHandler(SocketHandler):
    """A ``SocketHandler`` preconfigured to send messages as datagrams to a syslog service
    """

    def __init__(
            self,
            facility: Optional[int]=syslog.LOG_USER,
            host: Optional[str]='localhost',
            port: Optional[int]=514,
            encoding: Optional[str]='utf8',
            name: Optional[str]=None,
            level: Optional[LogLevel]=None
    ):
        """Instantiates a new ``SyslogHandler``

        :param facility: the syslog facility
        :param host: the hostname of the syslog server
        :param port: the port of the syslog server
        :param encoding: the message encoding
        :param name: the name of the handler
        :param level: the minimum verbosity level to write log entries
        """
        self.facility = facility
        super().__init__(
            name=name, level=level, host=host, port=port, family=socket.AF_INET,
            type=socket.SOCK_DGRAM, encoding=encoding)

    def write(self, message: str, level: LogLevel) -> None:
        """Writes the full log entry to the configured syslog endpoint

        :param message: the entire message to be written, full formatted
        :param level: the priority level of the message
        """
        if level >= self.min_level:
            priority = self._get_priority(level)
            message = f'<{priority}>{message}\000'
            self.socket.sendall(bytes(message, self.encoding))

    def _get_priority(self, level: LogLevel) -> int:
        """Gets the computed syslog priority value for the priority level

        :param level: the message's priority value
        :returns: the computed syslog priority value

        .. seealso:: https://tools.ietf.org/html/rfc5424
        .. seealso:: http://www.kiwisyslog.com/help/syslog/index.html?protocol_levels.htm
        """
        priority = (self.facility * 8) + level.as_syslog
        return priority

    def _create_name(self) -> str:
        """Creates the name for the handler - called from ``__init__`` if a name is not given.

        :returns: the template `syslog-{facility}`
        """
        return f'syslog-{self.facility}'
