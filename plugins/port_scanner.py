"""
Plugin : Scanner de ports TCP
Démontre un plugin utile avec scope obligatoire.
"""
import socket
from sdk import PluginBase, PluginMetadata


class PortScannerPlugin(PluginBase):
    """Scanner de ports TCP simple."""

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="Port Scanner",
            version="1.0.0",
            author="FOKAS",
            description="Scanne les ports TCP ouverts sur une cible.",
            category="attack",
            tags=["scan", "recon", "tcp"],
            requires_scope=True,
        )

    def run(self, config, args=None) -> dict:
        target = input("  [>] Cible (IP) : ").strip()
        if not target:
            return {"status": "error", "message": "Cible vide"}

        ports_input = input("  [>] Ports (ex: 22,80,443 ou 1-1024) [1-1024] : ").strip()
        if not ports_input:
            ports_input = "1-1024"

        ports = self._parse_ports(ports_input)
        if not ports:
            return {"status": "error", "message": "Ports invalides"}

        print(f"\n  Scan de {target} sur {len(ports)} ports...\n")
        opened = []

        for port in ports:
            if self._check_port(target, port, timeout=0.5):
                print(f"  {C.GRN if False else ''}[+] Port {port} ouvert")
                opened.append(port)

        print(f"\n  {len(opened)} port(s) ouvert(s) sur {len(ports)} testés")
        return {"status": "success", "opened_ports": opened}

    def _parse_ports(self, spec: str) -> list:
        ports = []
        for part in spec.split(","):
            part = part.strip()
            if "-" in part:
                try:
                    start, end = part.split("-")
                    ports.extend(range(int(start), int(end) + 1))
                except ValueError:
                    continue
            elif part.isdigit():
                ports.append(int(part))
        return [p for p in ports if 1 <= p <= 65535]

    def _check_port(self, host: str, port: int, timeout: float = 1.0) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            result = sock.connect_ex((host, port))
            return result == 0
        except Exception:
            return False
        finally:
            sock.close()