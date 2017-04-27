import syslog

from logging2.levels import LogLevel


def test_str():
    assert str(LogLevel.debug) == 'DEBUG'
    assert str(LogLevel.info) == 'INFO'
    assert str(LogLevel.warning) == 'WARNING'
    assert str(LogLevel.error) == 'ERROR'
    assert str(LogLevel.exception) == 'EXCEPTION'


def test_lt():
    assert (
        LogLevel.debug
        < LogLevel.info
        < LogLevel.warning
        < LogLevel.error
        < LogLevel.exception
    )


def test_le():
    assert (
        LogLevel.debug
        <= LogLevel.info
        <= LogLevel.warning
        <= LogLevel.error
        <= LogLevel.exception
    )
    assert LogLevel.debug <= LogLevel.debug


def test_eq():
    assert LogLevel.debug == LogLevel.debug


def test_ge():
    assert (
        LogLevel.exception
        >= LogLevel.error
        >= LogLevel.warning
        >= LogLevel.info
        >= LogLevel.debug
    )
    assert LogLevel.debug >= LogLevel.debug


def test_gt():
    assert (
        LogLevel.exception
        > LogLevel.error
        > LogLevel.warning
        > LogLevel.info
        > LogLevel.debug
    )


def test_syslog_eq():
    assert LogLevel.debug.as_syslog == syslog.LOG_DEBUG
    assert LogLevel.info.as_syslog == syslog.LOG_INFO
    assert LogLevel.warning.as_syslog == syslog.LOG_WARNING
    assert LogLevel.error.as_syslog == syslog.LOG_ERR
