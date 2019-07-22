"""
Utility functions for the application
"""
from datetime import datetime


DATE_FORMAT_DEFAULT = "%Y-%m-%dT%H:%M:%SZ"
DATE_FORMAT_FALLBACK = "%Y-%m-%dT%H:%M:%S"


def date2str(date, date_format="%Y/%m/%d %H:%M:%S"):
    return datetime.strftime(date, date_format)


def str2date(datestr, date_formats=(DATE_FORMAT_DEFAULT,
                                    DATE_FORMAT_FALLBACK)):
    exc = None
    # support a single date format arg
    if not type(date_formats) is tuple:
        date_formats = [date_formats]

    for date_format in date_formats:
        try:
            return datetime.strptime(datestr, date_format)
        except ValueError as exc:
            pass
    raise exc

