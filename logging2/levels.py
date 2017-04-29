import syslog
from enum import Enum


class LogLevel(Enum):
    """A workflow control construct that enables setting a minimum level of verbosity for log entries.
    """

    debug: int = 0
    info: int = 1
    warning: int = 2
    error: int = 3
    exception: int = 4

    def __str__(self) -> str:
        """Stringifies the ``name`` of the ``LogLevel`` enum

        :returns: the name of the level in upper case
        """
        return self.name.upper()

    def __lt__(self, other: 'LogLevel') -> bool:
        """Checks if this ``LogLevel`` is less than another

        :param other: the other level to test against
        :returns: is this level is less than the other
        """
        return self.value < other.value

    def __le__(self, other: 'LogLevel') -> bool:
        """Checks if this ``LogLevel`` is less than or equal to another

        :param other: the other level to test against
        :returns: is this level is less than or equal to the other
        """
        return self.value <= other.value

    def __eq__(self, other: 'LogLevel') -> bool:
        """Checks if this ``LogLevel`` is equal to another

        :param other: the other level to test against
        :returns: is this level is equal to the other
        """
        return self.value == other.value

    def __ge__(self, other: 'LogLevel') -> bool:
        """Checks if this ``LogLevel`` is greater than or equal to another

        :param other: the other level to test against
        :returns: is this level is greater than or equal to the other
        """
        return self.value >= other.value

    def __gt__(self, other: 'LogLevel') -> bool:
        """Checks if this ``LogLevel`` is greater than another

        :param other: the other level to test against
        :returns: is this level is greater than the other
        """
        return self.value > other.value

    @property
    def as_syslog(self) -> int:
        """Translates the internal library value to its corresponding Syslog value.

        :returns: the corresponding Syslog value
        """
        if self == LogLevel.debug:
            return syslog.LOG_DEBUG
        elif self == LogLevel.info:
            return syslog.LOG_INFO
        elif self == LogLevel.warning:
            return syslog.LOG_WARNING
        else:
            return syslog.LOG_ERR
