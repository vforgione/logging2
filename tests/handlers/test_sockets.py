import os
import socket
import syslog

from logging2.handlers.sockets import SyslogHandler, TcpHandler, TcpIPv6Handler, \
    UdpHandler, UdpIPv6Handler, UnixSocketHandler
from logging2.levels import LogLevel


class TestSyslogHandler:
    def setup_method(self, method):
        self.host = 'localhost'
        self.port = 8514

        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))

        self.handler = SyslogHandler(host=self.host, port=self.port)

    def teardown_method(self, method):
        self.server.close()

    def test_write(self):
        message = 'Hello, world!'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        priority = self.handler._get_priority(LogLevel.info)
        msg = '<{}>{}\000'.format(priority, message)
        expected = [bytes(msg, 'utf8')]

        assert messages == expected

    def test_write_non_ascii(self):
        message = '안녕하세요'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        priority = self.handler._get_priority(LogLevel.info)
        msg = '<{}>{}\000'.format(priority, message)
        expected = [bytes(msg, 'utf8')]

        assert messages == expected

    def test_create_name(self):
        assert self.handler.name == 'syslog-{}'.format(syslog.LOG_USER)


class TestTcpHandler:
    def setup_method(self, method):
        self.host = 'localhost'
        self.port = 8089

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

        self.handler = TcpHandler(host=self.host, port=self.port)

    def teardown_method(self, method):
        self.server.close()

    def test_write(self):
        message = 'Hello, world!'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            connection, address = self.server.accept()
            data = connection.recv(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_write_non_ascii(self):
        message = '안녕하세요'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            connection, address = self.server.accept()
            data = connection.recv(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_create_name(self):
        assert self.handler.name == 'TCP {}:{}'.format(self.host, self.port)


class TestTcpIPv6Handler:
    def setup_method(self, method):
        self.host = 'localhost'
        self.port = 8089

        self.server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

        self.handler = TcpIPv6Handler(host=self.host, port=self.port)

    def teardown_method(self, method):
        self.server.close()

    def test_write(self):
        message = 'Hello, world!'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            connection, address = self.server.accept()
            data = connection.recv(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_write_non_ascii(self):
        message = '안녕하세요'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            connection, address = self.server.accept()
            data = connection.recv(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_create_name(self):
        assert self.handler.name == 'TCP {}:{}'.format(self.host, self.port)


class TestUdpHandler:
    def setup_method(self, method):
        self.host = 'localhost'
        self.port = 8089

        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))

        self.handler = UdpHandler(host=self.host, port=self.port)

    def teardown_method(self, method):
        self.server.close()

    def test_write(self):
        message = 'Hello, world!'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_write_non_ascii(self):
        message = '안녕하세요'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_create_name(self):
        assert self.handler.name == 'UDP {}:{}'.format(self.host, self.port)


class TestUdpIPv6Handler:
    def setup_method(self, method):
        self.host = 'localhost'
        self.port = 8089

        self.server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))

        self.handler = UdpIPv6Handler(host=self.host, port=self.port)

    def teardown_method(self, method):
        self.server.close()

    def test_write(self):
        message = 'Hello, world!'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_write_non_ascii(self):
        message = '안녕하세요'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_create_name(self):
        assert self.handler.name == 'UDP {}:{}'.format(self.host, self.port)


class TestUnixHandler:
    def setup_method(self, method):
        self.node = '/tmp/unix.node'
        if os.path.exists(self.node):
            os.remove(self.node)

        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server.bind(self.node)

        self.handler = UnixSocketHandler(node=self.node)

    def teardown_method(self, method):
        self.server.close()

    def test_write(self):
        message = 'Hello, world!'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_write_non_ascii(self):
        message = '안녕하세요'
        self.handler.write(message, level=LogLevel.info)

        messages = []
        while True:
            data, address = self.server.recvfrom(1024)
            if len(data) > 0:
                messages.append(data)
                break

        expected = [bytes(message, 'utf8')]
        assert messages == expected

    def test_create_name(self):
        assert self.handler.name == 'UNIX {}'.format(self.node)
