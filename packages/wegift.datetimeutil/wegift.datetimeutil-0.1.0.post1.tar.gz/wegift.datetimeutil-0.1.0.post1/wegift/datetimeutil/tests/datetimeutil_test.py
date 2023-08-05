"""Test `wegift.datetimeutil`.
"""

import datetime

import wegift.datetimeutil


def test_parse_rfc7231_datetime_is_timezone_aware():
    """Test parsing timestamp in RFC 7231 format produces time zone aware
    datetime object.
    """
    formatted_timestamp = 'Fri, 21 Feb 2020 12:38:05 GMT'
    timestamp = wegift.datetimeutil.parse_rfc7231_datetime(formatted_timestamp)

    assert timestamp.tzinfo is datetime.timezone.utc
    date_to_match = datetime.datetime(year=2020, month=2, day=21, hour=12, minute=38,
                                      second=5, tzinfo=datetime.timezone.utc)
    assert timestamp == date_to_match


def test_parse_rfc7231_datetime_with_non_utc_timezone():
    """Test parsing timestamp in RFC 7231 format with other than UTC time zone.
    """
    formatted_timestamp = 'Fri, 21 Feb 2020 12:38:05 +0500'
    timestamp = wegift.datetimeutil.parse_rfc7231_datetime(formatted_timestamp)

    assert timestamp.tzinfo == datetime.timezone(datetime.timedelta(hours=5))
    date_to_match = datetime.datetime(year=2020, month=2, day=21, hour=12, minute=38, second=5,
                                      tzinfo=datetime.timezone(datetime.timedelta(hours=5)))
    assert timestamp == date_to_match


def test_format_rfc7231_datetime_with_utc_timezone():
    """Test formatting timestamp as RFC 7231 with UTC time zone.
    """
    timestamp = datetime.datetime(year=2020, month=2, day=21, hour=12, minute=38, second=5,
                                  tzinfo=datetime.timezone.utc)
    formatted_timestamp = wegift.datetimeutil.format_rfc7231_datetime(timestamp)

    assert formatted_timestamp == 'Fri, 21 Feb 2020 12:38:05 GMT'


def test_format_rfc7231_datetime_with_non_utc_timezone():
    """Test formatting timestamp as RFC 7231 with other than UTC time zone.
    """
    timestamp = datetime.datetime(year=2020, month=2, day=21, hour=17, minute=38, second=5,
                                  tzinfo=datetime.timezone(datetime.timedelta(hours=5)))
    formatted_timestamp = wegift.datetimeutil.format_rfc7231_datetime(timestamp)

    assert formatted_timestamp == 'Fri, 21 Feb 2020 12:38:05 GMT'


def test_unix_timestamp_to_datetime_with_utc_timezone():
    """Test converting UNIX timestamp to datetime with UTC time zone.
    """
    actual_timestamp = datetime.datetime(year=2020, month=2, day=21, hour=17, minute=38, second=5,
                                         tzinfo=datetime.timezone.utc)
    unix_timestamp = actual_timestamp.timestamp()

    assert wegift.datetimeutil.unix_timestamp_to_datetime(unix_timestamp) == actual_timestamp


def test_unix_timestamp_to_datetime_with_non_utc_timezone():
    """Test converting UNIX timestamp to datetime with other than UTC time
    zone.
    """
    actual_timestamp = datetime.datetime(year=2020, month=2, day=21, hour=17, minute=38, second=5,
                                         tzinfo=datetime.timezone(datetime.timedelta(hours=5)))
    unix_timestamp = actual_timestamp.timestamp()

    assert wegift.datetimeutil.unix_timestamp_to_datetime(unix_timestamp) == actual_timestamp
