"""Tests pour core/scope.py"""
import os
import json
import datetime

from core.scope import ScopeValidator


class TestScopeValidator:
    def test_initialization(self, temp_dir, monkeypatch):
        monkeypatch.chdir(temp_dir)
        sv = ScopeValidator()
        assert sv.active_scope is None

    def test_load_scope_no_file(self, temp_dir, monkeypatch):
        monkeypatch.chdir(temp_dir)
        sv = ScopeValidator()
        assert sv.load_scope() is None

    def test_load_scope_valid(self, temp_dir, monkeypatch):
        monkeypatch.chdir(temp_dir)
        os.makedirs("output", exist_ok=True)

        # Crée un scope valide
        scope = {
            "target": "127.0.0.1",
            "auth_ref": "test@example.com",
            "created_at": datetime.datetime.utcnow().isoformat(),
            "expires_at": (datetime.datetime.utcnow() +
                           datetime.timedelta(hours=24)).isoformat(),
            "hours": 24,
        }
        with open("output/active_scope.json", "w") as f:
            json.dump(scope, f)

        sv = ScopeValidator()
        loaded = sv.load_scope()
        assert loaded is not None
        assert loaded["target"] == "127.0.0.1"

    def test_load_scope_expired(self, temp_dir, monkeypatch):
        monkeypatch.chdir(temp_dir)
        os.makedirs("output", exist_ok=True)

        # Crée un scope expiré
        scope = {
            "target": "127.0.0.1",
            "auth_ref": "test@example.com",
            "created_at": (datetime.datetime.utcnow() -
                           datetime.timedelta(hours=48)).isoformat(),
            "expires_at": (datetime.datetime.utcnow() -
                           datetime.timedelta(hours=24)).isoformat(),
            "hours": 24,
        }
        with open("output/active_scope.json", "w") as f:
            json.dump(scope, f)

        sv = ScopeValidator()
        assert sv.load_scope() is None