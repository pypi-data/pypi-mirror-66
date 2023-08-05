"""Util functions to work with timezone aware timestamps.
"""

import datetime
import email.utils
from typing import Optional, Union

import arrow
import arrow.parser
import pytz


# WARNING
# -------
#
# Do not ever pass pytz timezone as `tzinfo` to datetime. It is safe to use
# `datetime.timezone.utc` with `tzinfo`, but for pytz timezone, use pytz
# timezone function `localize()`.


def get_tzinfo(timezone: str) -> datetime.tzinfo:
    """Get timezone information for given full time zone name.

    :param timezone: Full time zone name.
    :return: Timezone information.
    """
    return pytz.timezone(timezone)


def make_utc_datetime(year: int,  # pylint: disable=too-many-arguments
                      month: int,
                      day: int,
                      hour: int = 0,
                      minute: int = 0,
                      second: int = 0,
                      microsecond: int = 0) -> datetime.datetime:
    """Make timezone aware UTC datetime.

    :param year: Year.
    :param month: Month (between 1 and 12).
    :param day: Day (between 1 and number of days in the given month and year).
    :param hour: Hour (between 0 and 23).
    :param minute: Minute (between 0 and 59).
    :param second: Second (between 0 and 59).
    :param microsecond: Microsecond (between 0 and 1000000).
    :return: Datetime instance with timezone set to UTC.
    """
    return datetime.datetime(year, month, day, hour, minute, second, microsecond,
                             tzinfo=datetime.timezone.utc)


def make_utc_time(hour: int = 0,
                  minute: int = 0,
                  second: int = 0,
                  microsecond: int = 0) -> datetime.time:
    """Make timezone aware UTC time.

    :param hour: Hour (between 0 and 23).
    :param minute: Minute (between 0 and 59).
    :param second: Second (between 0 and 59).
    :param microsecond: Microsecond (between 0 and 1000000).
    :return: Time instance with timezone set to UTC.
    """
    return datetime.time(hour, minute, second, microsecond,
                         tzinfo=datetime.timezone.utc)


def utcnow() -> datetime.datetime:
    """Return current UTC time as timezone aware timestamp.

    :return: Timezone aware datetime.
    """
    return datetime.datetime.now(datetime.timezone.utc)


def now(timezone: Union[str, datetime.tzinfo]) -> datetime.datetime:
    """Return current time in the given timezone.

    :param timezone: Full time zone name or timezone info.
    :return: Timezone aware datetime.
    """
    if isinstance(timezone, str):
        # It is safe to pass pytz timezone to `.now()`.
        return datetime.datetime.now(pytz.timezone(timezone))

    return datetime.datetime.now(timezone)


def utctoday() -> datetime.datetime:
    """Return current UTC date as timezone aware timestamp with time set to UTC
    midnight.

    :return: Timezone aware datetime.
    """
    return floor_day_resolution(utcnow())


def utctoday_naive() -> datetime.date:
    """Return current UTC date without timezone information.

    :return: Date without timezone information.
    """
    return utcnow().date()


def utcdate(year: int, month: int, day: int) -> datetime.datetime:
    """Construct timezone aware datetime for the midnight of given day.

    :param year: Year.
    :param month: Month.
    :param day: Day.
    :return: Timezone aware datetime.
    """
    return datetime.datetime(year, month, day,
                             tzinfo=datetime.timezone.utc)


def parse_timestamp(formatted_timestamp: str,
                    timestamp_format: Optional[str] = None) -> datetime.datetime:
    """Parse formatted timestamp string into timezone aware datetime object.

    If formatted timestamp doesn't have timezone information, UTC is assumed.

    :param formatted_timestamp: Formatted timestamp to parse.
    :param timestamp_format: Parse formatted timestamp according to this format. If not provided,
    format is guessed.
    :return: Timezone aware datetime.
    :raises ValueError: if timestamp could not be parsed either with given
    format or could not be guessed if format was not given.
    """
    if timestamp_format is None:
        # Guess format.
        try:
            return arrow.get(formatted_timestamp).datetime
        except arrow.parser.ParserError as exception:
            raise ValueError(str(exception))

    return datetime.datetime.strptime(formatted_timestamp,
                                      timestamp_format).replace(tzinfo=datetime.timezone.utc)


def unix_timestamp_to_datetime(unix_timestamp: float) -> datetime.datetime:
    """Convert UNIX timestamp to UTC datetime. UTC timezone is assumed.

    :param unix_timestamp: UNIX timestamp.
    :return: Timezone aware datetime.
    """
    return datetime.datetime.fromtimestamp(unix_timestamp, datetime.timezone.utc)


def format_date_gb(timestamp: Union[datetime.date, datetime.datetime]) -> str:
    """Format date according to United Kingdom date format: DD/MM/YYYY.

    :param timestamp: Date to format.
    :return: Formatted date (DD/MM/YYYY).
    """
    return timestamp.strftime('%d/%m/%Y')


def format_datetime_gb(timestamp: Union[datetime.date, datetime.datetime]) -> str:
    """Format date time according to United Kingdom date time format:
    DD/MM/YYYY HH:MM.

    :param timestamp: Date to format.
    :return: Formatted date (DD/MM/YYYY).
    """
    return timestamp.strftime('%d/%m/%Y %H:%M')


def format_iso8601_z(timestamp: datetime.datetime, sep='T', timespec='auto') -> str:
    """Format timestamp according to ISO 8601 and use 'Z' as representation of an offset of zero.

    :param sep: A one-character separator, placed between the date and time portions of the result.
    :param timespec: Specifies the number of additional components of the time to include (the
    default is 'auto'). Please refer to `datetime.datetime.isoformat()` documentation for details.
    :return: ISO 8601 formatted timestamp.
    """
    assert isinstance(timestamp, datetime.datetime), f'{type(timestamp)}'
    if timestamp.utcoffset() is None:
        return timestamp.replace(tzinfo=None).isoformat(sep=sep, timespec=timespec) + 'Z'
    return timestamp.isoformat(sep=sep, timespec=timespec)


def localize(tzinfo: datetime.tzinfo, timestamp: datetime.datetime) -> datetime.datetime:
    """Add timezone information to naive timestamp. It doesn't change time,
    only adds tzinfo.

    :param tzinfo: Use the timezone information to attach to timestamp.
    :param timestamp: Localize this timestamp.
    :return: Timezone aware timestamp.
    """
    assert timestamp.tzinfo is None
    if hasattr(tzinfo, 'localize'):
        return tzinfo.localize(timestamp)  # type: ignore
    return timestamp.replace(tzinfo=tzinfo)


def calculate_start_of_day(date: datetime.date,
                           tzinfo: datetime.tzinfo = datetime.timezone.utc) -> datetime.datetime:
    """Convert date to datetime at midnight same day. UTC is assumed.

    :param date: Date.
    :param tzinfo: Calculate start of day in the given timezone. Defaults to
    UTC.
    :return: Timezone aware UTC timestamp.
    """
    return localize(tzinfo,
                    datetime.datetime(date.year, date.month, date.day))


def calculate_end_of_day(date: datetime.date,
                         tzinfo: datetime.tzinfo = datetime.timezone.utc) -> datetime.datetime:
    """For the given day calculate datetime that has time as close to midnight
    next day as possible. UTC is assumed.

    :param date: Date.
    :param tzinfo: Calculate end of day in the given timezone. Defaults to UTC.
    :return: Timezone aware UTC timestamp.
    """
    return (calculate_start_of_day(date, tzinfo) +
            datetime.timedelta(days=1) -
            datetime.timedelta(microseconds=1))


def calculate_start_of_month_naive(date: datetime.date) -> datetime.date:
    """For the given date reset the day to 1, so it's a start of a month.

    :param date: Date.
    :return: Naive date.
    """
    return datetime.date(date.year, date.month, 1)


def calculate_start_of_quarter_period_naive(date: datetime.date) -> datetime.date:
    """For the given date return the day 1 of the quarter period

    :param date: Date
    :return: Naive date
    """

    first_days_for_quarters_in_date_year = (
        datetime.date(year=date.year, month=1, day=1),
        datetime.date(year=date.year, month=4, day=1),
        datetime.date(year=date.year, month=7, day=1),
        datetime.date(year=date.year, month=10, day=1)
    )
    quarter_of_the_year_index = ((date.month - 1) // 3)

    return first_days_for_quarters_in_date_year[quarter_of_the_year_index]


def ceil_day_resolution(timestamp: datetime.datetime) -> datetime.datetime:
    """Calculate timestamp ceiling in day resolution.

    If timestamp is exactly at midnight, the same value is returned. Otherwise
    the ceiling of timestamp is next day midnight.

    :param timestamp: Timestamp.
    :return: Timestamp.
    """
    midnight = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
    return timestamp if midnight == timestamp else midnight + datetime.timedelta(days=1)


def floor_day_resolution(timestamp: datetime.datetime) -> datetime.datetime:
    """Calculate timestamp floor in day resolution.

    If timestamp is exactly at midnight, the same value is returned. Otherwise
    the floor of timestamp is same day midnight.

    :param timestamp: Timestamp.
    :return: Timestamp.
    """
    return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)


def to_datetime(date_or_datetime: Union[datetime.date, datetime.datetime],
                tzinfo: datetime.tzinfo = datetime.timezone.utc) -> datetime.datetime:
    """Convert date to datetime. It assumed that datetime is already timezone
    aware.

    The use of this function is discouraged. It's kept for legacy code where
    randomly date vs datetime is used.

    :param date_or_datetime: Date or datetime instance.
    :param tzinfo: Timezone information. Defaults to UTC.
    :return: Timezone aware datetime instance with time set to midnight if
    input was date. If it was datetime, unmodified value is returned.
    """
    if isinstance(date_or_datetime, datetime.date):
        return calculate_start_of_day(date_or_datetime, tzinfo=tzinfo)

    assert date_or_datetime.tzinfo is not None

    return date_or_datetime


def format_rfc7231_datetime(timestamp: datetime.datetime) -> str:
    """Formats the timestamp according to RFC 7231 format.

    :param timestamp: Timestamp to be formatted.
    :return: RFC 7231 formatted timestamp
    """
    return email.utils.format_datetime(timestamp.astimezone(datetime.timezone.utc), usegmt=True)


def parse_rfc7231_datetime(formatted_timestamp: str) -> datetime.datetime:
    """Parses the RFC 7231 timestamp to datetime.

    :param formatted_timestamp: Formatted timestamp to parse.
    :return: Parsed datetime object.
    """
    return email.utils.parsedate_to_datetime(formatted_timestamp)
