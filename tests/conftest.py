"""
FOKARAT - Configuration pytest
Fixtures partagées pour tous les tests.
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

import pytest

# Ajoute la racine du projet au PYTHONPATH
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture
def temp_dir():
    """Crée un dossier temporaire pour les tests."""
    tmp = tempfile.mkdtemp(prefix="fokarat_test_")
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def temp_config(temp_dir):
    """Retourne une config temporaire."""
    from core.config import Config

    config_path = os.path.join(temp_dir, "config.yaml")
    config = Config(config_file=config_path)
    config.set("output_dir", os.path.join(temp_dir, "output"))
    config.set("lhost", "127.0.0.1")
    config.set("lport", 4444)
    return config


@pytest.fixture
def sample_python_code():
    """Code Python simple pour tester l'obfuscation."""
    return '''
def hello():
    print("Hello, FOKARAT!")

if __name__ == "__main__":
    hello()
'''


@pytest.fixture
def sample_c_code():
    """Code C simple pour tester le padding."""
    return '''
#include <stdio.h>

int main() {
    printf("Hello, FOKARAT!\\n");
    return 0;
}
'''