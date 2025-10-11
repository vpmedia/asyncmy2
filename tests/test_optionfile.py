from configparser import NoOptionError, NoSectionError

import pytest

from asyncmy.optionfile import Parser


def test_parser():
    parser = Parser()
    parser.add_section("test")
    parser.set("test", "single_quoted", "'value1'")
    parser.set("test", "double_quoted", '"value2"')
    parser.set("test", "unquoted", "value3")
    assert parser.get("test", "single_quoted") == "value1"
    assert parser.get("test", "double_quoted") == "value2"
    assert parser.get("test", "unquoted") == "value3"
    # no section test
    with pytest.raises(NoSectionError):
        parser.get("missing", "option")
    # no option test
    with pytest.raises(NoOptionError):
        parser.get("test", "missing_option")
