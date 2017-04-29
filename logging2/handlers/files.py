import codecs
import re
from codecs import StreamReaderWriter
from typing import Optional

from logging2.handlers.abc import Handler
from logging2.levels import LogLevel


# NOTE: This module does not provide handlers for rotating log files. The rationale behind that is that all *NIX systems
# have software specifically designed to do that, and it's much faster and reliable. Let's separate
# concerns here: this logging software is meant to be both Pythonic and fast. There's nothing Pythonic or fast about
# reinventing the wheel. A great utility is ``logrotate``, which is available for Debian, Red Hat, and BSD systems.

# Linux Manpage: https://linux.die.net/man/8/logrotate
# FreeBSD Manpage: https://www.freebsd.org/cgi/man.cgi?query=logrotate&manpath=SuSE+Linux/i386+11.3


class FileHandler(Handler):
    """A type of ``Handler`` that writes messages to a file on the local system
    """

    def __init__(
            self,
            file_path: str,
            mode: Optional[str] = 'a',
            encoding: Optional[str] = 'utf8',
            errors: Optional[str] = 'strict',
            buffering: Optional[int] = 1,
            name: Optional[str] = None,
            level: Optional[LogLevel] = None
    ):
        """Instantiates a new ``FileHandler``

        :param file_path: the path (full or relative) to the log file
        :param mode: the file mode
        :param encoding: the file encoding
        :param errors: how should errors be handled
        :param buffering: should the line be buffered
        :param name: the name of the handler
        :param level: the minimum level of verbosity/priority of the messages this will log
        """
        self.fh: StreamReaderWriter = codecs.open(
            file_path, mode=mode, encoding=encoding, errors=errors,
            buffering=buffering)
        super().__init__(name=name, level=level)
        self.encoding: str = encoding

    def write(self, message: str, level: LogLevel) -> None:
        """Writes the full log entry to the configured file

        :param message: the entire message to be written, full formatted
        :param level: the priority level of the message
        """
        if level >= self.min_level:
            self.fh.write(bytes(message, self.encoding).decode(self.encoding))
            self.fh.flush()

    def _create_name(self) -> str:
        """Creates the name for the handler - called from ``__init__`` if a name is not given.

        :returns: the name of the file
        """
        fname = self.fh.name.split('/')[-1]
        return re.sub('[^\w.]', '', str(fname))
