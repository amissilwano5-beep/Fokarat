#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$ROOT_DIR/Framework/Framework"

POSSIBLE_VENVS=(
  "$ROOT_DIR/.venv"
  "$PROJECT_DIR/venv"
  "$ROOT_DIR/venv"
)

VENV_DIR=""
for venv in "${POSSIBLE_VENVS[@]}"; do
  if [ -f "$venv/bin/activate" ] && [ -f "$venv/bin/python" ]; then
    VENV_DIR="$venv"
    break
  fi
done

if [ -z "$VENV_DIR" ]; then
  echo "[!] Aucun virtualenv trouvé."
  echo "    Crée un environnement avec : python3 -m venv .venv"
  exit 1
fi

if [ "$#" -eq 0 ]; then
  ARGS="--cli"
else
  ARGS="$@"
fi

cd "$PROJECT_DIR"
source "$VENV_DIR/bin/activate"
python main.py $ARGS
