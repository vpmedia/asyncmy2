# ChangeLog

## 0.2

### 0.2.18

- Exclude the `benchmark` and `examples` folder from the package distribution.

### 0.2.17

- Added frozen dependency installation for uv.
- First release with Trusted Publisher workflow.

### 0.2.16

- Generate MacOS Intel wheels.

### 0.2.15

- Bumped pypa/cibuildwheel version to v3.2.0.

### 0.2.14

- Added handling of cancelled tasks while execution in progress. ([#108](https://github.com/long2ice/asyncmy/pull/108))

### 0.2.13

- Added missing wheel publishing for Windows platform.

### 0.2.12

- Migrated from poetry to uv with pdm backend. ([#136](https://github.com/long2ice/asyncmy/pull/136))
- Fixed security vulnerability with escape_dict converter. ([CVE-2024-36039](https://github.com/advisories/GHSA-v9hf-5j83-6xpp))
- Added OSError exception handling to connection getpass.getuser() for Python 3.13+ compatibility. ([#133](https://github.com/long2ice/asyncmy/pull/133))
- Fixed deprecated VALUES regexp syntax issue. ([#120](https://github.com/long2ice/asyncmy/pull/120))
- Changed connection pool behavior to send QUIT message while closing connections. ([#113](https://github.com/long2ice/asyncmy/pull/113))
- Improved MacOS development environment support.
- Fixed pytest asyncio test runner issues with latest version.
- Bumped python and github workflow dependency versions.

### 0.2.11

- Fix `'Connection' object has no attribute '_auth_plugin_name'` (#86)

### 0.2.10

- Fix ssl context pass bool.
- Fix missing `*.whl` for Python 3.12 (#94)
- Fix SSL handshake error with MySQL server v8.0.34+. (#80)

### 0.2.9

- Added support for SSL context creation via `ssl` parameter using a dictionary containing `mysql_ssl_set` parameters. (
  #64)
- Fix bug with fallback encoder in the `escape_item()` function. (#65)

### 0.2.8

- Fix sudden loss of float precision. (#56)
- Fix pool `echo` parameter not apply to create connection. (#62)
- Fix replication reconnect.

### 0.2.7

- Fix `No module named 'asyncmy.connection'`.

### 0.2.6

- Fix raise_mysql_exception (#28)
- Implement `read_timeout` and remove `write_timeout` parameters (#44)

### 0.2.5

- Revert `TIME` return `datetime.time` object. (#37)

### 0.2.4

- Fix `escape_string` for enum type. (#30)
- `TIME` return `datetime.time` object.

### 0.2.3

- Fix `escape_sequence`. (#20)
- Fix `connection.autocommit`. (#21)
- Fix `_clear_result`. (#22)

### 0.2.2

- Fix bug. (#18)
- Fix replication error.

### 0.2.1

- Fix `binlogstream` await. (#12)
- Remove `loop` argument. (#15)
- Fix `unix_socket` connect. (#17)

### 0.2.0

- Fix `cursor.close`.

## 0.1

### 0.1.9

- Force int `pool_recycle`.
- Fix `echo` option.
- Fix bug replication and now don't need to connect manual.

### 0.1.8

- Fix pool recycle. (#4)
- Fix async `fetchone`, `fetchall`, and `fetchmany`. (#7)

### 0.1.7

- Fix negative pk. (#2)

### 0.1.6

- Bug fix.

### 0.1.5

- Remove `byte2int` and `int2byte`.
- Fix warning for sql_mode.

### 0.1.4

- Add replication support.

### 0.1.3

- Fix pool.

### 0.1.2

- Fix build error.

### 0.1.1

- Fix build error.

### 0.1.0

- Release first version.
