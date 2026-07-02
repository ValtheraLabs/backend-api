#!/usr/bin/env sh
set -eu
python -m ruff check app tests
python -m black --check app tests
python -m mypy app tests
python -m pytest
