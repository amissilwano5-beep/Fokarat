"""
FOKARAT - Logger professionnel
Auteur: Lwano Amissi Blanchard (FOKAS)
Version: 1.0
"""

import os
import sys
import json
import datetime


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


class Logger:
    """
    Logger centralisé pour FOKARAT.
    - Affiche les messages en couleur dans le terminal.
    - Enregistre tous les événements dans un fichier JSON (fokarat.log).
    """

    def __init__(self, log_file="fokarat.log"):
        self.log_file = log_file
        self._ensure_log_file()

    def _ensure_log_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("")

    def _write_to_file(self, level, message, **kwargs):
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "level": level,
            "message": message,
        }
        entry.update(kwargs)
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def info(self, message, **kwargs):
        print(f"{Colors.CYAN}[*]{Colors.RESET} {message}")
        self._write_to_file("INFO", message, **kwargs)

    def success(self, message, **kwargs):
        print(f"{Colors.GREEN}[+]{Colors.RESET} {message}")
        self._write_to_file("SUCCESS", message, **kwargs)

    def warning(self, message, **kwargs):
        print(f"{Colors.YELLOW}[!]{Colors.RESET} {message}")
        self._write_to_file("WARNING", message, **kwargs)

    def error(self, message, **kwargs):
        print(f"{Colors.RED}[-]{Colors.RESET} {message}", file=sys.stderr)
        self._write_to_file("ERROR", message, **kwargs)

    def debug(self, message, **kwargs):
        print(f"{Colors.MAGENTA}[D]{Colors.RESET} {message}")
        self._write_to_file("DEBUG", message, **kwargs)

    def banner(self, text):
        print(f"{Colors.BOLD}{Colors.GREEN}{text}{Colors.RESET}")