"""Tests pour core/utils.py"""
import os

from core.utils import ensure_dir, get_local_ip, which


class TestUtils:
    def test_which_existing_command(self):
        # python3 doit exister
        assert which("python3") is not None or which("python") is not None

    def test_which_nonexistent_command(self):
        assert which("commande_qui_nexiste_pas_12345") is None

    def test_get_local_ip(self):
        ip = get_local_ip()
        assert isinstance(ip, str)
        assert len(ip) > 0

    def test_ensure_dir_creates_directory(self, temp_dir):
        new_dir = os.path.join(temp_dir, "new", "nested", "dir")
        result = ensure_dir(new_dir)

        assert os.path.exists(new_dir)
        assert os.path.isdir(new_dir)
        assert result == new_dir

    def test_ensure_dir_existing_directory(self, temp_dir):
        # Ne doit pas planter si le dossier existe
        result = ensure_dir(temp_dir)
        assert result == temp_dir