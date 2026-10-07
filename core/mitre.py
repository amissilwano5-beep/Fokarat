"""
FOKARAT - Mapping MITRE ATT&CK
Associe chaque action du framework à une technique MITRE.
"""
from core.logger import Logger

logger = Logger()


# ══════════════════════════════════════════════════
#  MAPPING MITRE ATT&CK
# ══════════════════════════════════════════════════
MITRE_TECHNIQUES = {
    # Initial Access
    "phishing_badusb": {
        "id": "T1566.001",
        "tactic": "Initial Access",
        "name": "Spearphishing via USB",
        "description": "Injection via périphérique USB (BadUSB).",
    },
    "usb_drive": {
        "id": "T1091",
        "tactic": "Initial Access",
        "name": "Replication Through Removable Media",
        "description": "Propagation via support amovible.",
    },

    # Execution
    "cmd_execution": {
        "id": "T1059.003",
        "tactic": "Execution",
        "name": "Command and Scripting Interpreter: Windows Command Shell",
        "description": "Exécution via cmd.exe.",
    },
    "powershell_execution": {
        "id": "T1059.001",
        "tactic": "Execution",
        "name": "Command and Scripting Interpreter: PowerShell",
        "description": "Exécution via PowerShell.",
    },
    "python_execution": {
        "id": "T1059.006",
        "tactic": "Execution",
        "name": "Command and Scripting Interpreter: Python",
        "description": "Exécution via Python.",
    },
    "uac_bypass": {
        "id": "T1548.002",
        "tactic": "Privilege Escalation",
        "name": "Bypass User Account Control",
        "description": "Contournement UAC via fodhelper.exe.",
    },

    # Persistence
    "wmi_persistence": {
        "id": "T1546.003",
        "tactic": "Persistence",
        "name": "Event Triggered Execution: WMI Event Subscription",
        "description": "Persistance via abonnement WMI.",
    },
    "registry_persistence": {
        "id": "T1547.001",
        "tactic": "Persistence",
        "name": "Registry Run Keys / Startup Folder",
        "description": "Persistance via registre.",
    },

    # Defense Evasion
    "obfuscation": {
        "id": "T1027",
        "tactic": "Defense Evasion",
        "name": "Obfuscated Files or Information",
        "description": "Obfuscation du code (XOR + zlib + base64).",
    },
    "padding": {
        "id": "T1027.009",
        "tactic": "Defense Evasion",
        "name": "Embedded Payloads",
        "description": "Padding aléatoire pour casser les signatures.",
    },
    "upx_pack": {
        "id": "T1027.002",
        "tactic": "Defense Evasion",
        "name": "Software Packing",
        "description": "Compression UPX du binaire.",
    },
    "anti_vm": {
        "id": "T1497.001",
        "tactic": "Defense Evasion",
        "name": "Virtualization/Sandbox Evasion: System Checks",
        "description": "Détection de VM/sandbox.",
    },
    "anti_debug": {
        "id": "T1622",
        "tactic": "Defense Evasion",
        "name": "Debugger Evasion",
        "description": "Détection de debugger.",
    },
    "multi_encoder": {
        "id": "T1027.013",
        "tactic": "Defense Evasion",
        "name": "Encrypted/Encoded File",
        "description": "Multi-encodage MSFVenom.",
    },

    # Discovery
    "port_scan": {
        "id": "T1046",
        "tactic": "Discovery",
        "name": "Network Service Discovery",
        "description": "Scan de ports TCP.",
    },

    # Command and Control
    "reverse_shell": {
        "id": "T1071.001",
        "tactic": "Command and Control",
        "name": "Application Layer Protocol: Web Protocols",
        "description": "Reverse shell via HTTP/TCP.",
    },
    "msf_handler": {
        "id": "T1071",
        "tactic": "Command and Control",
        "name": "Application Layer Protocol",
        "description": "Handler Metasploit.",
    },
    "http_c2": {
        "id": "T1071.001",
        "tactic": "Command and Control",
        "name": "Application Layer Protocol: Web Protocols",
        "description": "C2 via HTTP.",
    },

    # Impact
    "data_exfil": {
        "id": "T1041",
        "tactic": "Exfiltration",
        "name": "Exfiltration Over C2 Channel",
        "description": "Exfiltration de fichiers.",
    },
}


class MitreMapper:
    """Génère des rapports MITRE ATT&CK."""

    def __init__(self):
        self.techniques = MITRE_TECHNIQUES

    def get(self, key):
        return self.techniques.get(key, {})

    def list_all(self):
        """Liste toutes les techniques connues."""
        return self.techniques

    def generate_report(self, actions, output_path=None):
        """
        Génère un rapport MITRE à partir d'une liste d'actions.
        actions = liste de clés (ex: ['padding', 'wmi_persistence'])
        """
        lines = [
            "# 🎯 Rapport MITRE ATT&CK - FOKARAT",
            "",
            f"**Total d'actions mappées :** {len(actions)}",
            "",
            "## Techniques utilisées",
            "",
            "| ID | Tactic | Technique | Description |",
            "|----|--------|-----------|-------------|",
        ]

        seen = set()
        tactics = {}

        for action in actions:
            tech = self.techniques.get(action)
            if not tech or tech["id"] in seen:
                continue
            seen.add(tech["id"])
            lines.append(
                f"| {tech['id']} | {tech['tactic']} | {tech['name']} | {tech['description']} |"
            )
            tactics.setdefault(tech["tactic"], []).append(tech["id"])

        # Résumé par tactique
        lines += ["", "## Résumé par tactique", ""]
        for tactic, ids in sorted(tactics.items()):
            lines.append(f"- **{tactic}** : {len(ids)} technique(s) — {', '.join(ids)}")

        # Fichier MITRE Navigator
        lines += ["", "## Fichier MITRE Navigator", ""]
        lines.append("Un fichier JSON compatible avec le MITRE Navigator peut être généré.")
        lines.append("Utilisez l'option `[34]` pour l'exporter.")

        content = "\n".join(lines)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.success(f"Rapport MITRE : {output_path}")

        return content

    def export_navigator_json(self, actions, output_path):
        """Exporte un fichier JSON pour le MITRE Navigator."""
        import json

        techniques = []
        for action in actions:
            tech = self.techniques.get(action)
            if tech:
                techniques.append({
                    "techniqueID": tech["id"],
                    "tactic": tech["tactic"].lower().replace(" ", "-"),
                    "score": 100,
                    "color": "#ff6666",
                    "comment": tech["description"],
                })

        data = {
            "name": "FOKARAT Session",
            "versions": {"attack": "14", "navigator": "4.9.0", "layer": "4.5"},
            "domain": "enterprise-attack",
            "description": "Techniques utilisées dans une session FOKARAT",
            "techniques": techniques,
            "gradient": {
                "colors": ["#ffffff", "#ff6666"],
                "minValue": 0,
                "maxValue": 100,
            },
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.success(f"Fichier Navigator : {output_path}")
        return output_path