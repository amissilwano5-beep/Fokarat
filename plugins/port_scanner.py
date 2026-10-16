"""
Plugin : Scanner de ports TCP
Non-interactif — utilise args pour les paramètres.
Le scope est vérifié automatiquement par PluginBase.
"""
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from sdk import PluginBase, PluginMetadata


class PortScannerPlugin(PluginBase):
    """Scanner de ports TCP multithread avec vérification de scope."""

    DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445,
                     993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 6379,
                     8080, 8443, 27017]

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="Port Scanner",
            version="2.0.0",
            author="FOKAS",
            description="Scan TCP multithread (non-interactif, scope requis).",
            category="attack",
            tags=["scan", "recon", "tcp"],
            requires_scope=True,
            target_param="target",
        )

    def _execute(self, config, args=None) -> dict:
        # Extrait les paramètres (pas de input() !)
        if not args or not isinstance(args, dict):
            return {"status": "error", "message": "args requis (dict)"}

        target = args.get("target")
        ports_input = args.get("ports", "top")
        timeout = float(args.get("timeout", 0.5))
        threads = int(args.get("threads", 100))

        if not target:
            return {"status": "error", "message": "target manquant"}

        # Parse les ports
        if ports_input == "top":
            ports = self.DEFAULT_PORTS
        elif isinstance(ports_input, str):
            ports = self._parse_ports(ports_input)
        elif isinstance(ports_input, list):
            ports = [int(p) for p in ports_input if 1 <= int(p) <= 65535]
        else:
            return {"status": "error", "message": "ports invalide"}

        if not ports:
            return {"status": "error", "message": "aucun port valide"}

        # Scan multithread
        opened = []
        with ThreadPoolExecutor(max_workers=threads) as ex:
            futures = {ex.submit(self._check_port, target, p, timeout): p for p in ports}
            for fut in as_completed(futures):
                port = futures[fut]
                try:
                    if fut.result():
                        opened.append(port)
                except Exception:
                    pass

        opened.sort()

        return {
            "status": "success",
            "target": target,
            "scanned": len(ports),
            "opened_ports": opened,
            "opened_count": len(opened),
        }

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

    def _check_port(self, host: str, port: int, timeout: float) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            return sock.connect_ex((host, port)) == 0
        except Exception:
            return False
        finally:
            sock.close()