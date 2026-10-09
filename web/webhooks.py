"""
FOKARAT - Webhooks SIEM/SOAR
Envoie les événements vers Splunk, Elastic, etc.
"""
import os
import json
import time
import threading
import queue
from datetime import datetime

from core.logger import Logger

logger = Logger()


class WebhookManager:
    """
    Gestionnaire de webhooks asynchrones.
    File d'attente interne + envoi via requests en arrière-plan.
    """

    def __init__(self, config=None):
        self.config = config
        self.queue = queue.Queue()
        self._worker = None
        self._stop = threading.Event()
        self.hooks = []  # liste de URLs

        # Charge les webhooks depuis config
        if config:
            urls = config.get("webhooks", [])
            if isinstance(urls, list):
                self.hooks = urls

    def add_hook(self, url: str):
        if url and url not in self.hooks:
            self.hooks.append(url)
            logger.success(f"Webhook ajouté : {url}")

    def remove_hook(self, url: str):
        if url in self.hooks:
            self.hooks.remove(url)
            logger.info(f"Webhook retiré : {url}")

    def start(self):
        """Démarre le worker asynchrone."""
        if self._worker and self._worker.is_alive():
            return
        self._stop.clear()
        self._worker = threading.Thread(target=self._run, daemon=True)
        self._worker.start()
        logger.info("Webhook manager démarré")

    def stop(self):
        self._stop.set()
        if self._worker:
            self._worker.join(timeout=2)
        logger.info("Webhook manager arrêté")

    def emit(self, event_type: str, data: dict):
        """Envoie un événement à tous les webhooks."""
        if not self.hooks:
            return
        payload = {
            "framework": "FOKARAT",
            "event": event_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": data,
        }
        self.queue.put(payload)

    def _run(self):
        while not self._stop.is_set():
            try:
                payload = self.queue.get(timeout=1)
                self._send(payload)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erreur webhook worker : {e}")

    def _send(self, payload):
        try:
            import requests
        except ImportError:
            logger.warning("requests non installé, webhooks désactivés")
            return

        for url in self.hooks:
            try:
                r = requests.post(
                    url,
                    json=payload,
                    timeout=5,
                    headers={"Content-Type": "application/json"},
                )
                if r.status_code < 400:
                    logger.success(f"Webhook envoyé : {url}")
                else:
                    logger.warning(f"Webhook {url} : HTTP {r.status_code}")
            except Exception as e:
                logger.warning(f"Webhook {url} échec : {e}")


# Instance globale (initialisée avec la config dans main)
webhook_manager = WebhookManager()