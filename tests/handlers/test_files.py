import codecs
import os

from logging2.handlers.files import FileHandler
from logging2.levels import LogLevel


class TestFileHandler:
    def setup_method(self, method):
        self.filename = '/tmp/test_file_handler.log'
        self.handler = FileHandler(self.filename)

    def teardown_method(self, method):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_write(self):
        message = 'Hello, world!'
        self.handler.write(message, level=LogLevel.info)
        with codecs.open(self.filename, 'r', encoding='utf8') as fh:
            output = [line for line in fh]
        assert output == [message]

    def test_write_non_ascii(self):
        message = '안녕하세요'
        self.handler.write(message, level=LogLevel.info)
        with codecs.open(self.filename, 'r', encoding='utf8') as fh:
            output = [line for line in fh]
        assert output == [message]

    def test_create_name(self):
        assert self.handler.name == 'test_file_handler.log'
