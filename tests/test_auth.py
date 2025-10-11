from asyncmy.auth import scramble_native_password


def test_scramble_native_password():
    password = "secret"
    salt = "key"
    result = scramble_native_password(password.encode("utf-8"), salt.encode("utf-8"))
    assert result == b"q\x8d\xb0\x92\xa8\xa9\xb6\x9b\xc9\x16\xc1\x0e\xcf\xd5\x18vj\xf4S\xf6"
