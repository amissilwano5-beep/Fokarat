#!/bin/bash
# FOKARAT - Installation complète

set -e

echo "=== Installation des outils système ==="
sudo apt update
sudo apt install -y python3-pip python3-venv git g++ mingw-w64 ncat \
    apktool default-jdk zipalign binutils-avr upx-ucl make build-essential

echo "=== Création de l'environnement virtuel ==="
python3 -m venv .venv
source .venv/bin/activate

echo "=== Installation des dépendances Python ==="
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov pytest-mock ruff black mypy pre-commit bandit
pip install fastapi uvicorn pyinstaller

echo "=== Installation des hooks pre-commit ==="
pre-commit install

echo "=== Vérification ==="
make --version
ruff --version
black --version
pytest --version

echo ""
echo "✅ Installation terminée !"
echo "Lance FOKARAT avec : ./run.sh"