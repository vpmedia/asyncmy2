import re

import pytest

from asyncmy.connection import Connection
from asyncmy.constants.SERVER_STATUS import SERVER_STATUS_NO_BACKSLASH_ESCAPES
from asyncmy.errors import OperationalError
from conftest import connection_kwargs


@pytest.mark.asyncio
async def test_connect():
    connection = Connection(**connection_kwargs)
    await connection.connect()
    assert connection._connected
    assert re.match(
        r"\d+\.\d+\.\d+([^0-9].*)?",
        connection.get_server_info(),
    )
    assert connection.get_proto_info() == 10
    assert connection.get_host_info() != "Not Connected"
    await connection.ensure_closed()


@pytest.mark.asyncio
async def test_read_timeout():
    with pytest.raises(OperationalError):
        connection = Connection(read_timeout=1, **connection_kwargs)
        await connection.connect()
        async with connection.cursor() as cursor:
            await cursor.execute("DO SLEEP(3)")


@pytest.mark.parametrize("no_backslash_escapes", [False, True])
@pytest.mark.asyncio
async def test_escape_honours_no_backslash_escapes(no_backslash_escapes):
    """Every parameter shape must be quoted for the server's current sql_mode.

    Under NO_BACKSLASH_ESCAPES a backslash is an ordinary character, so escaping
    ``'`` as ``\\'`` leaves the literal open and the rest of the value is parsed as
    SQL. escape() was the only escaper consulting the flag, so bytes values and
    members of sequences stayed backslash-escaped and were injectable.
    """
    conn = Connection(**connection_kwargs)
    conn.server_status = SERVER_STATUS_NO_BACKSLASH_ESCAPES if no_backslash_escapes else 0
    payload = "' OR 1=1 -- "
    expected = "''' OR 1=1 -- '" if no_backslash_escapes else "'\\' OR 1=1 -- '"

    assert conn.escape(payload) == expected
    assert conn.escape(payload.encode()) == expected
    assert conn.escape(bytearray(payload.encode())) == expected
    # A sequence parameter, as used by `WHERE id IN %s`: its members are escaped
    # by converters.escape_item(), one level below escape().
    assert conn.literal((payload,)) == f"({expected})"
    assert conn.literal((payload.encode(),)) == f"({expected})"


@pytest.mark.asyncio
async def test_escape_bytes_binary_prefix():
    """The _binary prefix is opt-in; it used to be emitted unconditionally."""
    assert Connection(**connection_kwargs).escape(b"ab") == "'ab'"
    assert Connection(binary_prefix=True, **connection_kwargs).escape(b"ab") == "_binary'ab'"


@pytest.mark.asyncio
async def test_transaction(connection):
    await connection.begin()
    await connection.query(
        """INSERT INTO test.asyncmy(`decimal`, date, datetime, `float`,
         string, `tinyint`) VALUES (%s,'%s','%s',%s,'%s',%s)"""
        % (
            1,
            "2020-08-08",
            "2020-08-08 00:00:00",
            1,
            "1",
            1,
        ),
        True,
    )
    await connection.rollback()
