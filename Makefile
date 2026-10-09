.PHONY: help install install-dev test test-fast test-cov lint format type-check security clean build run all

help:
	@echo "FOKARAT - Commandes disponibles :"
	@echo ""
	@echo "  make install       Installer les dépendances de production"
	@echo "  make install-dev   Installer les dépendances de développement"
	@echo "  make test          Lancer les tests (sans couverture)"
	@echo "  make test-cov      Lancer les tests avec couverture"
	@echo "  make test-fast     Lancer les tests rapides"
	@echo "  make lint          Vérifier le code avec ruff"
	@echo "  make format        Formater le code"
	@echo "  make type-check    Vérifier les types avec mypy"
	@echo "  make security      Scanner la sécurité avec bandit"
	@echo "  make clean         Nettoyer les fichiers temporaires"
	@echo "  make build         Construire le package"
	@echo "  make run           Lancer FOKARAT"
	@echo "  make all           Lint + Type + Test"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest

test-cov:
	pytest --cov=core --cov=modules --cov=ai --cov-report=term-missing --cov-report=html:output/coverage_html

test-fast:
	pytest -m "not slow"

lint:
	ruff check .

format:
	ruff format .
	black .

type-check:
	mypy core modules ai

security:
	bandit -r core modules ai -c pyproject.toml

clean:
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

run:
	./run.sh

all: lint type-check test
	@echo "✓ Toutes les vérifications sont passées"