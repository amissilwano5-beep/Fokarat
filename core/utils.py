"""FOKARAT - Fonctions utilitaires"""
import os
import sys
import socket
import subprocess
import shutil


def which(program):
    """Vérifie si un programme est dans le PATH."""
    return shutil.which(program)


def get_local_ip():
    """Détecte l'IP locale."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def ask_lhost_lport(config):
    """Demande LHOST et LPORT à l'utilisateur, ou utilise la config existante."""
    default_ip = config.get("lhost") or get_local_ip()
    lhost = input(f"  [>] LHOST (IP d'écoute) [{default_ip}] : ").strip()
    if not lhost:
        lhost = default_ip
    config.set("lhost", lhost)

    default_port = config.get("lport", 4444)
    lport_raw = input(f"  [>] LPORT (port d'écoute) [{default_port}] : ").strip()
    if not lport_raw:
        lport = int(default_port)
    else:
        try:
            lport = int(lport_raw)
            if not (1 <= lport <= 65535):
                raise ValueError
        except ValueError:
            print("  [!] LPORT invalide, utilisation de 4444.")
            lport = 4444
    config.set("lport", lport)
    return lhost, lport


def ensure_dir(path):
    """Crée un dossier s'il n'existe pas."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path


def safe_input(prompt):
    """Input sécurisé contre Ctrl+C."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[!] Interruption.")
        return ""