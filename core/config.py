"""
FOKARAT - Gestionnaire de configuration
Auteur: Lwano Amissi Blanchard (FOKAS)
Version: 1.0
"""

import os
import yaml


class Config:
    """
    Gère la configuration de FOKARAT.
    Les valeurs sont lues depuis config.yaml et peuvent être modifiées
    dynamiquement par l'utilisateur via le menu.
    """

    DEFAULTS = {
        "lhost": "",
        "lport": 4444,
        "http_server_port": 8080,
        "output_dir": "output",
        "network_mode": "tcp",
        "android_keystore": "my.keystore",
        "android_apk_input": "",
        "llm_model_path": "models/mistral-7b.gguf",
        "stealth_mode": False,
        "persistence_method": "wmi",
        "usb_method": "ducky",
    }

    def __init__(self, config_file="config.yaml"):
        self.config_file = config_file
        self.data = dict(self.DEFAULTS)
        self.load()

    def load(self):
        """Charge la configuration depuis le fichier YAML."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded = yaml.safe_load(f) or {}
                    self.data.update(loaded)
            except Exception as e:
                print(f"[!] Erreur de lecture de config: {e}")

    def save(self):
        """Sauvegarde la configuration dans le fichier YAML."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(self.data, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            print(f"[!] Erreur d'écriture de config: {e}")
            return False

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value

    def get_local_network_ip(self):
        """Détecte l'IP locale de la machine (pour suggérer un LHOST)."""
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def __repr__(self):
        return yaml.dump(self.data, default_flow_style=False, allow_unicode=True)