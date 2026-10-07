"""Tests pour core/ethics.py"""
import os
import json
import datetime

from core.ethics import EthicsController


class TestEthicsController:
    def test_initial_state(self, temp_dir, monkeypatch):
        monkeypatch.chdir(temp_dir)
        ethics = EthicsController()
        assert ethics.dry_run is False
        assert ethics.killed is False

    def test_enable_dry_run(self, temp_dir, monkeypatch):
        monkeypatch.chdir(temp_dir)
        ethics = EthicsController()
        ethics.enable_dry_run()
        assert ethics.dry_run is True

    def test_disable_dry_run(self, temp_dir, monkeypatch):
        monkeypatch.chdir(temp_dir)
        ethics = EthicsController()
        ethics.enable_dry_run()
        ethics.disable_dry_run()
        assert ethics.dry_run is False

    def test_audit_creates_log(self, temp_dir, monkeypatch):
        monkeypatch.chdir(temp_dir)
        os.makedirs("output", exist_ok=True)

        ethics = EthicsController()
        ethics.audit("TEST_ACTION", "details de test")

        assert os.path.exists("output/audit.log")
        with open("output/audit.log", "r", encoding="utf-8") as f:
            line = f.readline()
            entry = json.loads(line)

        assert entry["action"] == "TEST_ACTION"
        assert entry["details"] == "details de test"

    def test_confirm_action_dry_run(self, temp_dir, monkeypatch):
        monkeypatch.chdir(temp_dir)
        ethics = EthicsController()
        ethics.enable_dry_run()

        # En dry-run, pas besoin de confirmation utilisateur
        assert ethics.confirm_action("test") is True