checkfiles = asyncmy/ tests/ examples/ conftest.py build.py
py_warn = PYTHONDEVMODE=1
MYSQL_PASS ?= "123456"

UNAME_S := $(shell uname -s)

# Required to build mysqlclient on MacOS
ifeq ($(UNAME_S),Darwin)
	export PKG_CONFIG_PATH := /opt/homebrew/opt/mysql-client/lib/pkgconfig
endif

# Load env variables
ifneq (,$(wildcard ./.env))
	include .env
    export
endif

up:
	@uv lock --upgrade

deps:
	@uv sync --all-groups --all-extras $(options)

_style:
	@uv run ruff format $(checkfiles)
	@uv run ruff check --fix $(checkfiles)

style: deps _style

_check:
	@uv run ruff format --check $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	@uv run ruff check $(checkfiles)
	@uv run mypy $(checkfiles)

check: deps _check

_test:
	$(py_warn) MYSQL_PASS=$(MYSQL_PASS) uv run pytest

test: deps _test

clean:
	@rm -rf *.so && rm -rf build && rm -rf dist && rm -rf asyncmy/*.c && rm -rf asyncmy/*.so && rm -rf asyncmy/*.html

build: clean
	@uv build

benchmark: deps
	@python benchmark/main.py

ci: deps _check _test
