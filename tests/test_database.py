"""Tests pour core/database.py"""
import os

from core.database import Database


class TestDatabase:
    def test_database_creates_file(self, temp_dir):
        db_path = os.path.join(temp_dir, "test.db")
        Database(db_path=db_path)
        assert os.path.exists(db_path)

    def test_log_payload(self, temp_dir):
        db_path = os.path.join(temp_dir, "test.db")
        db = Database(db_path=db_path)

        # Crée un faux fichier
        fake_payload = os.path.join(temp_dir, "fake.exe")
        with open(fake_payload, "wb") as f:
            f.write(b"x" * 1024)

        db.log_payload("python", "127.0.0.1", 4444, fake_payload, "success")

        payloads = db.get_all_payloads()
        assert len(payloads) == 1
        assert payloads[0][2] == "python"
        assert payloads[0][3] == "127.0.0.1"
        assert payloads[0][4] == 4444

    def test_log_listener(self, temp_dir):
        db_path = os.path.join(temp_dir, "test.db")
        db = Database(db_path=db_path)

        db.log_listener("ncat", "0.0.0.0", 4444, "-", "running")

        listeners = db.get_all_listeners()
        assert len(listeners) == 1
        assert listeners[0][2] == "ncat"

    def test_export_report(self, temp_dir):
        db_path = os.path.join(temp_dir, "test.db")
        db = Database(db_path=db_path)
        db.log_listener("ncat", "0.0.0.0", 4444, "-", "running")

        report_path = os.path.join(temp_dir, "report.md")
        db.export_report(path=report_path)

        assert os.path.exists(report_path)
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "Rapport d'opérations" in content
        assert "ncat" in content