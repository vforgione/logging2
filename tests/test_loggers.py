import pytest
import re
from capturer import CaptureOutput
from uuid import uuid4

from logging2.handlers.streaming import StdErrHandler, StdOutHandler
from logging2.levels import LogLevel
from logging2.loggers import Logger


_timestamp_group = "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}[+-]\d{2}:\d{2}"
_level_group = "[A-Z]+"
_name_group = "\w+"
_message_group = "[^\n]+"
BASIC_OUTPUT_REGEX = re.compile(
    f"^{_timestamp_group} {_level_group} {_name_group}: {_message_group}"
)


class TestLogger:
    @classmethod
    def setup_class(cls):
        cls.logger = Logger(name="test", level=LogLevel.debug)

    def test_debug(self):
        message = "Hello, World!"

        with CaptureOutput() as co:
            self.logger.debug(message)
        output = co.get_text()

        assert BASIC_OUTPUT_REGEX.match(output)

    def test_info(self):
        message = "Hello, World!"

        with CaptureOutput() as co:
            self.logger.info(message)
        output = co.get_text()

        assert BASIC_OUTPUT_REGEX.match(output)

    def test_warning(self):
        message = "Hello, World!"

        with CaptureOutput() as co:
            self.logger.warning(message)
        output = co.get_text()

        assert BASIC_OUTPUT_REGEX.match(output)

    def test_error(self):
        message = "Hello, World!"

        with CaptureOutput() as co:
            self.logger.error(message)
        output = co.get_text()

        assert BASIC_OUTPUT_REGEX.match(output)

    def test_exception(self):
        message = "Hello, World!"

        with CaptureOutput() as co:
            try:
                1 / 0
            except ZeroDivisionError:
                self.logger.exception(message)
        output = co.get_text()

        assert BASIC_OUTPUT_REGEX.match(output)

    def test_init_with_one_handler(self):
        handler = StdErrHandler(name="test-stderr")
        logger = Logger(name="test-handler", handler=handler)

        assert logger.handlers == [handler]

    def test_init_with_multiple_handlers(self):
        handler0 = StdErrHandler(name="test-stderr")
        handler1 = StdOutHandler(name="test-stdout")
        logger = Logger(name="test-handlers", handlers=[handler0, handler1])
        assert logger.handlers == [handler0, handler1]

    def test_init_already_registered(self):
        logger = Logger(name="test")

        assert logger.name == self.logger.name
        assert logger.handlers == self.logger.handlers
        assert logger.template == self.logger.template
        assert logger.keys == self.logger.keys

    def test_set_template(self):
        logger = Logger(name="template")
        assert logger.template == Logger.DEFAULT_TEMPLATE

        template = "{timestamp} {message}"
        keys = {"timestamp", "message"}
        logger.template = template

        assert logger.template == template
        assert logger.keys == keys

        with CaptureOutput() as co:
            logger.info("Hello, world!")
        output = co.get_text()

        regex = f"{_timestamp_group} {_message_group}"
        assert re.match(regex, output)

    def test_remove_handler(self):
        handler = StdErrHandler()
        self.logger.add_handler(handler)

        assert len(self.logger.handlers) == 2

        self.logger.remove_handler("stderr")

        assert len(self.logger.handlers) == 1
        assert isinstance(self.logger.handlers[0], StdOutHandler)

    def test_get_exec_info(self):
        template = "{source} {line} {function} {process}: {message}"
        logger = Logger(name="exec-info", template=template)

        with CaptureOutput() as co:
            logger.info("hello")
        output = co.get_text()

        regex = "[\w/]+\.py \d+ \w+ \d+: [^\n]+"
        assert re.match(regex, output)

    def test_additional_context_static(self):
        template = "{name} {person}: {message}"
        logger = Logger(
            name="ad-static", template=template, additional_context={"person": "vince"}
        )

        with CaptureOutput() as co:
            logger.info("hello")
        output = co.get_text()

        assert output == "ad-static vince: hello"

    def test_additional_context_function(self):
        template = "{uuid} {message}"
        logger = Logger(
            name="ad-func", template=template, additional_context={"uuid": uuid4}
        )

        with CaptureOutput() as co:
            logger.info("hello")
        output = co.get_text()

        assert re.match(
            "[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12} hello",
            output,
        )

    def test_log_with_context_static(self):
        with CaptureOutput() as co:
            self.logger.info("Hello", timestamp="now")
        output = co.get_text()

        assert not BASIC_OUTPUT_REGEX.match(output)
        assert output.startswith("now")

    def test_log_with_context_func(self):
        def get_timestamp():
            return "now"

        with CaptureOutput() as co:
            self.logger.info("Hello", timestamp=get_timestamp)
        output = co.get_text()

        assert not BASIC_OUTPUT_REGEX.match(output)
        assert output.startswith("now")

    def test_init_no_keys(self):
        with pytest.raises(ValueError):
            template = "ohai"
            Logger(name="no-keys", template=template)
