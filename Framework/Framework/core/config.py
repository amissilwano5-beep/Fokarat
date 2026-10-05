import os
import yaml
import socket
from typing import Any, Dict

class Config:
    DEFAULT = {
        "kali_ip": "auto",
        "kali_port": 4444,
        "network_mode": "tcp",
        "network_protocol": "tcp",
        "http_server_port": 8080,
        "https_server_port": 8443,
        "payload_url": "",
        "llm_model_path": "models/mistral-7b.gguf",
        "usb_method": "ducky",
        "persistence_method": "wmi",
        "android_keystore": "my.keystore",
        "android_keystore_pass": "password",
        "android_alias": "myalias",
        "ios_exploit_cve": "CVE-2025-31200",
        "ai_enabled": True,
        "ai_model": "mistral-7b"
    }

    def __init__(self, path: str = "config.yaml"):
        self.path = path
        self.data = self._load()
        if not os.path.exists(path):
            self.save()

    @staticmethod
    def get_local_network_ip() -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            pass

        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except Exception:
            pass

        try:
            for family, _, _, _, sockaddr in socket.getaddrinfo(socket.gethostname(), None):
                if family == socket.AF_INET:
                    ip = sockaddr[0]
                    if not ip.startswith("127."):
                        return ip
        except Exception:
            pass

        return "192.168.1.100"

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                for key, value in self.DEFAULT.items():
                    data.setdefault(key, value)
                return data
        return self.DEFAULT.copy()

    def get(self, key: str, default=None):
        value = self.data.get(key, default)
        if key in ("kali_ip", "listen_ip") and (value in (None, "", "auto")):
            return self.get_local_network_ip()
        if key in ("network_mode", "network_protocol") and value in (None, ""):
            return "tcp"
        return value

    def set(self, key: str, value):
        self.data[key] = value

    def save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, f, default_flow_style=False)