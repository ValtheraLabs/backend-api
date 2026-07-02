.PHONY: install dev test lint format typecheck check docker-up docker-down

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff check app tests

format:
	black app tests
	ruff check --fix app tests

typecheck:
	mypy app tests

check: lint typecheck test

docker-up:
	docker compose up --build

docker-down:
	docker compose down
