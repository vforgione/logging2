==========
 logging2
==========

A More Pythonic Logging System *or* You Deserve Better Than ``log4j``


-------------------------------
 The Basic Contract of Logging
-------------------------------

Logging should be simple and intuitive.

For most use cases, you want to quickly instantiate a logger and dump some text
to a stream. You would expect a common workflow based on a minimum level of
verbosity in the log entries and for those entries to be formatted in some
fashion that is both human readable and machine parseable. There should also be
a set of common metadata that can be used to provide context to the entry.

That context should also be easily extended to suit everyone's use cases.
Additionally, the values passed to that context should be pliable - users should
have the option to override those values as they deem necessary.

Common meta information should conform to as widely adopted standards as
possible - i.e. ISO 8601 timestamps and full unicode supported messages.

As stated foremost, the interface to this system should be simple and
intuitive. This means the complexity of the system should be minimized,
configuration should have sane defaults and the supporting library should
be packed with expressive documentation.

Implementation of the Contract
------------------------------

The user should only be concerned with three components:

- Verbosity (``LogLevel``)
- Message Producers (``Handler``)
- Message Creation (``Logger``)
