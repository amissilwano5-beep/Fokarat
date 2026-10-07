"""
FOKARAT - Base de données SQLite
Enregistre toutes les opérations du framework.
"""
import os
import sqlite3
import json
import datetime
from core.logger import Logger

logger = Logger()


class Database:

    def __init__(self, db_path="output/fokarat.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS payloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    type TEXT NOT NULL,
                    lhost TEXT,
                    lport INTEGER,
                    output_path TEXT,
                    size_bytes INTEGER,
                    status TEXT,
                    metadata TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS listeners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    type TEXT NOT NULL,
                    lhost TEXT,
                    lport INTEGER,
                    payload TEXT,
                    status TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    target_ip TEXT,
                    payload_type TEXT,
                    notes TEXT
                )
            """)

    def log_payload(self, payload_type, lhost, lport, path, status, metadata=None):
        size = os.path.getsize(path) if path and os.path.exists(path) else 0
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO payloads (timestamp, type, lhost, lport, output_path, size_bytes, status, metadata) "
                "VALUES (?,?,?,?,?,?,?,?)",
                (datetime.datetime.utcnow().isoformat(), payload_type, lhost, lport,
                 path, size, status, json.dumps(metadata or {}))
            )
        logger.info(f"Payload enregistré en DB : {payload_type}")

    def log_listener(self, ltype, lhost, lport, payload, status):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO listeners (timestamp, type, lhost, lport, payload, status) "
                "VALUES (?,?,?,?,?,?)",
                (datetime.datetime.utcnow().isoformat(), ltype, lhost, lport, payload, status)
            )

    def get_all_payloads(self):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT * FROM payloads ORDER BY id DESC").fetchall()

    def get_all_listeners(self):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT * FROM listeners ORDER BY id DESC").fetchall()

    def export_report(self, path="output/fokarat_report.md"):
        payloads = self.get_all_payloads()
        listeners = self.get_all_listeners()

        lines = [
            "# FOKARAT - Rapport d'opérations\n",
            f"*Généré le {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*\n",
            "\n## Payloads générés\n",
        ]
        if payloads:
            lines += [
                "| Date | Type | LHOST | LPORT | Taille | Statut |",
                "|------|------|-------|-------|--------|--------|",
            ]
            for p in payloads:
                lines.append(f"| {p[1][:16]} | {p[2]} | {p[3]} | {p[4]} | {p[6]} o | {p[7]} |")
        else:
            lines.append("*Aucun payload généré.*")

        lines += ["\n## Listeners\n"]
        if listeners:
            lines += [
                "| Date | Type | LHOST | LPORT | Payload |",
                "|------|------|-------|-------|---------|",
            ]
            for l in listeners:
                lines.append(f"| {l[1][:16]} | {l[2]} | {l[3]} | {l[4]} | {l[5]} |")
        else:
            lines.append("*Aucun listener enregistré.*")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        logger.success(f"Rapport exporté : {path}")
        return path