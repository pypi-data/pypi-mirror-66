#logger_adacore package

A very basic Python package provides a subclass of logging.Formatter.

Subclass JSONFormatter is capable to log a string or an ordered dict.

The only possible JSON format is as following for this version of the package:
{
    "asctime": "2020-04-26 20:26:38,471",
    "levelname": "INFO",
    "msg": "testing logging format"
}
