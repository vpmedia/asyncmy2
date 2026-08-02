import datetime

import pytest
from asyncmy.converters import (
    convert_date,
    convert_datetime,
    convert_time,
    convert_timedelta,
    escape_dict,
    escape_item,
    escape_str,
)


class CustomDate(datetime.date):
    pass


def test_escape_item():
    assert escape_item("\\\n\r\032\"'foobar\0", "utf-8") == "'\\\\\\n\\r\\Z\\\"\\'foobar\\0'"
    assert escape_item(datetime.date(2023, 6, 2), "utf-8") == "'2023-06-02'"
    assert escape_item(CustomDate(2023, 6, 2), "utf-8") == "'2023-06-02'"


def test_escape_str():
    assert escape_str("\\\n\r\032\"'foobar\0") == "'\\\\\\n\\r\\Z\\\"\\'foobar\\0'"

    # The encoder for the str type is a default encoder,
    # so it should accept values that are not strings as well.
    assert escape_str(datetime.date(2023, 6, 2)) == "'2023-06-02'"
    assert escape_str(CustomDate(2023, 6, 2)) == "'2023-06-02'"


def test_escape_unsigned_big_int():
    with pytest.raises(OverflowError):
        assert escape_item(2**64 - 1, "utf-8") == str(2**64 - 1)
        assert escape_item(0, "utf-8") == str(0)


def test_escape_dict_keys():
    """Test that dict keys are properly escaped (CVE-2025-65896 / CVE-2024-36039).

    Dict keys must be escaped the same way as values, otherwise SQL
    injection is possible via crafted dict keys.
    """
    malicious_key = "foo'; DROP TABLE users; --"
    result = escape_dict({malicious_key: "bar"}, "utf-8")
    assert malicious_key not in result
    assert "foo\\'; DROP TABLE users; --" in result

    result = escape_dict({"key'with\"quotes": "value"}, "utf-8")
    assert "key\\'with\\\"quotes" in result

    result = escape_dict({"key\\with\\backslash": "value"}, "utf-8")
    assert "key\\\\with\\\\backslash" in result

    result = escape_dict({"name": "test", "id": 123}, "utf-8")
    assert result["name"] == "'test'"
    assert result["id"] == "123"


def test_convert_date():
    assert convert_date("2007-02-26") == datetime.date(2007, 2, 26)
    assert convert_date(b"2007-02-26") == datetime.date(2007, 2, 26)
    assert convert_date(bytearray(b"2007-02-26")) == datetime.date(2007, 2, 26)


def test_convert_datetime():
    assert convert_datetime("2007-02-25 23:06:20") == datetime.datetime(2007, 2, 25, 23, 6, 20)
    assert convert_datetime("2007-02-25T23:06:20") == datetime.datetime(2007, 2, 25, 23, 6, 20)
    assert convert_datetime("2007-02-25 23:06:20.123456") == datetime.datetime(
        2007, 2, 25, 23, 6, 20, 123456
    )
    assert convert_datetime(b"2007-02-25 23:06:20") == datetime.datetime(2007, 2, 25, 23, 6, 20)


def test_convert_time():
    assert convert_time("15:06:17") == datetime.time(15, 6, 17)
    assert convert_time(b"15:06:17") == datetime.time(15, 6, 17)


def test_convert_timedelta():
    assert convert_timedelta("25:06:17") == datetime.timedelta(hours=25, minutes=6, seconds=17)
    assert convert_timedelta("-25:06:17") == -datetime.timedelta(hours=25, minutes=6, seconds=17)
    assert convert_timedelta(b"25:06:17") == datetime.timedelta(hours=25, minutes=6, seconds=17)


@pytest.mark.parametrize(
    "converter,value",
    [
        # Zero dates, as used by legacy schemas (DATE NOT NULL DEFAULT '0000-00-00').
        (convert_date, "0000-00-00"),
        (convert_datetime, "0000-00-00 00:00:00"),
        # Dates that parse but do not exist.
        (convert_date, "2007-02-31"),
        (convert_datetime, "2007-02-31T23:06:20"),
        # Values the regexes reject outright.
        (convert_datetime, "random crap"),
        (convert_time, "-25:06:17"),
        (convert_time, "random crap"),
        (convert_timedelta, "random crap"),
    ],
)
def test_convert_illegal_value_returns_raw(converter, value):
    """Illegal values fall back to the raw string instead of raising.

    Declaring these converters with a concrete Cython return type made the
    fallback raise `TypeError: Cannot convert str to datetime.date` at the C
    boundary, which aborted row conversion mid-packet and desynced the
    connection. See https://github.com/vpmedia/asyncmy2/issues/24.
    """
    assert converter(value) == value
    assert converter(value.encode()) == value
