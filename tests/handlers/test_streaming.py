import io

from capturer import CaptureOutput
from logging2.handlers.streaming import StdErrHandler, StdOutHandler, StreamingHandler
from logging2.levels import LogLevel


class TestStreamingHandler:
    def setup_method(self, method):
        self.stream = io.StringIO()
        self.handler = StreamingHandler(name="test", stream=self.stream)

    def test_write(self):
        message = "Hello, world!"
        self.handler.write(message, level=LogLevel.info)
        self.stream.seek(0)
        output = self.stream.getvalue()
        assert output == message

    def test_write_non_ascii(self):
        message = "안녕하세요"
        self.handler.write(message, level=LogLevel.info)
        self.stream.seek(0)
        output = self.stream.getvalue()
        assert output == message

    def test_create_name(self):
        handler = StreamingHandler(stream=self.stream, name=None)
        expected_name = "StringIO"
        assert handler.name == expected_name


class TestStdOutHandler:
    def setup_method(self, method):
        self.handler = StdOutHandler()

    def test_write(self):
        message = "Hello, world!"
        with CaptureOutput() as co:
            self.handler.write(message, level=LogLevel.info)
        output = co.get_text()
        assert output == message

    def test_write_non_ascii(self):
        message = "안녕하세요"
        with CaptureOutput() as co:
            self.handler.write(message, level=LogLevel.info)
        output = co.get_text()
        assert output == message


class TestStdErrHandler:
    def setup_method(self, method):
        self.handler = StdErrHandler()

    def test_write(self):
        message = "Hello, world!"
        with CaptureOutput() as co:
            self.handler.write(message, level=LogLevel.info)
        output = co.get_text()
        assert output == message

    def test_write_non_ascii(self):
        message = "안녕하세요"
        with CaptureOutput() as co:
            self.handler.write(message, level=LogLevel.info)
        output = co.get_text()
        assert output == message
