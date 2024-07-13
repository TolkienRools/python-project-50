#!/usr/bin/env python3

install:
	poetry install

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=gendiff --cov-report xml

