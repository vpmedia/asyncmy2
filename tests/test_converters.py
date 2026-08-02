import datetime

import pytest
from asyncmy.converters import escape_dict, escape_item, escape_str


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
