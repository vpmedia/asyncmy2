# Configuration
checkfiles = asyncmy/ tests/ examples/ conftest.py build.py
py_warn = PYTHONDEVMODE=1
MYSQL_PASS ?= "123456"

# Required to build mysqlclient on MacOS to run tests
UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S),Darwin)
	export PKG_CONFIG_PATH := /opt/homebrew/opt/mysql-client/lib/pkgconfig
endif

# Load env variables to override MySQL password
ifneq (,$(wildcard ./.env))
	include .env
    export
endif

# Upgrade packages
up:
	@uv lock --upgrade

# Install dependencies
deps:
	@if [ ! -f asyncmy/charset.c ]; then \
		echo "asyncmy not built yet, running uv with reinstall package..."; \
		uv sync --frozen --all-groups --all-extras --reinstall-package asyncmy2 $(options); \
	else \
		uv sync --frozen --all-groups --all-extras $(options); \
	fi

# Lint and format codebase
_style:
	@uv run ruff format $(checkfiles)
	@uv run ruff check --fix $(checkfiles)

style: deps _style

# Lint and check formatting issues without fixing
_check:
	@uv run ruff format --check $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	@uv run ruff check $(checkfiles)
	@uv run mypy $(checkfiles)

check: deps _check

# Run unit tests
_test:
	$(py_warn) MYSQL_PASS=$(MYSQL_PASS) uv run pytest

test: deps _test

# Clean build files
clean:
	@rm -rf *.so
	@rm -rf .pdm-build
	@rm -rf build
	@rm -rf dist
	@rm -rf asyncmy/*.c
	@rm -rf asyncmy/*.so
	@rm -rf asyncmy/*.html

# Build the project
build: clean
	@uv build

# Run project benchmarks
benchmark: deps
	MYSQL_PASS=$(MYSQL_PASS) uv run benchmark

# Run project examples
example: deps
	MYSQL_PASS=$(MYSQL_PASS) uv run examples/main.py
	MYSQL_PASS=$(MYSQL_PASS) uv run examples/sqla.py

# CI tasks (lint, format check, test)
ci: deps _check _test
