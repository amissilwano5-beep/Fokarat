<!-- ═══════════════════════════════════════════════════════════════ -->
<!--                            FOKARAT                              -->
<!-- ═══════════════════════════════════════════════════════════════ -->

<div align="center">

# 🛡️ FOKARAT

**Framework de cybersécurité éducatif — modulaire, éthique et open-source**

[![Version](https://img.shields.io/badge/version-3.4.0-brightgreen.svg?style=for-the-badge)](https://github.com/amissilwano5-beep/Fokarat/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Linux-orange.svg?style=for-the-badge&logo=linux&logoColor=white)](https://www.kali.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg?style=for-the-badge)]()
[![Made in RDC](https://img.shields.io/badge/Made%20in-RDC%20🇨🇩-yellow.svg?style=for-the-badge)]()

**Building the future, one tool at a time.**

[Documentation](DOCUMENTATION.md) •
[Installation](INSTALLATION.md) •
[Roadmap](ROADMAP.md) •
[Contribuer](CONTRIBUTING.md) •
[Signaler un bug](https://github.com/amissilwano5-beep/Fokarat/issues)

</div>

---

## 🎯 Qu'est-ce que FOKARAT ?

**FOKARAT** est un **framework de cybersécurité éducatif** développé depuis Bukavu (RDC) par [Lwano Amissi Blanchard (FOKAS)](https://github.com/amissilwano5-beep).

Inspiré de **TheFatRat** mais avec une **architecture moderne** (plugins, API REST, MITRE ATT&CK), FOKARAT permet d'apprendre les techniques offensives dans un cadre **strictement éthique et légal**.

> ⚠️ **FOKARAT est un outil ÉDUCATIF.** Toute utilisation sur des systèmes sans autorisation écrite est **illégale**.
> Lisez [DISCLAIMER.md](DISCLAIMER.md) avant toute utilisation.

---

## ✨ Fonctionnalités

### 🎯 Génération de payloads

| Module | Description |
|--------|-------------|
| **Python** | Reverse shell avec reconnexion automatique |
| **C++** | Cross-platform via Mingw (Windows 32/64) |
| **MSFVenom** | 8 types de payloads (Windows, Linux, Android, macOS, PHP, Python, Java) |

### 🎧 Listeners & C2

| Module | Description |
|--------|-------------|
| **ncat** | Listener Netcat moderne |
| **Metasploit** | Handler multi/payload automatique |
| **HTTP Server** | Serveur local pour payloads + exfiltration |

### 💾 BadUSB

| Module | Description |
|--------|-------------|
| **Générateur** | 5 types d'attaques (reverse shell, exfiltration, admin, download-exec) |
| **Encodeur** | Compilation `.duck` → `.bin` automatique |
| **Flasher** | Support Digispark, Raspberry Pi Pico, Rubber Ducky |
| **Furtif** | Contournement UAC via `fodhelper.exe` |
| **Layouts** | QWERTY (US/UK), AZERTY (FR), QWERTZ (DE/CH) |

### 🛡️ Évasion antivirus

| Module | Description |
|--------|-------------|
| **Padding aléatoire** | 16 Ko de code mort + 15 fonctions fake (signature unique à chaque compile) |
| **Obfuscation Python** | XOR + zlib + base64 + découpage multi-couches |
| **Compression UPX** | Mode ultra-brute (50-70% de réduction) |
| **Multi-encodage** | 7 encodeurs MSFVenom (shikata_ga_nai, xor_dynamic, etc.) |
| **Anti-VM** | 6 méthodes (fenêtres, drivers, RAM, CPU, hostname, username) |
| **Anti-Debug** | 5 méthodes (IsDebuggerPresent, PEB, timing, hardware breakpoints) |

### 📱 Attaques

| Module | Description |
|--------|-------------|
| **APK Injector** | Injection automatique de payload Metasploit dans un APK |
| **Persistance WMI** | Installation d'un abonnement WMI silencieux |

### 🌐 Infrastructure

| Module | Description |
|--------|-------------|
| **API REST** | FastAPI avec authentification JWT |
| **Plugins SDK** | Ajout de modules sans toucher au core |
| **Base SQLite** | Historique complet des opérations |
| **MITRE ATT&CK** | Mapping automatique + export Navigator |
| **Chiffrement AES** | Protection des secrets (AES-256-GCM) |
| **Sandbox** | Limites CPU/RAM/temps d'exécution |
| **Journal d'audit** | Chaque action est enregistrée (JSON) |
| **Mode DRY-RUN** | Simulation sans exécution réelle |
| **Kill switch** | Arrêt d'urgence via `Ctrl+C` |
| **Scope obligatoire** | Déclaration d'autorisation avant chaque attaque |

---

## 🚀 Installation rapide

```bash
# 1. Cloner le dépôt
git clone https://github.com/amissilwano5-beep/Fokarat.git
cd Fokarat

# 2. Installation automatique
chmod +x install.sh run.sh
./install.sh

# 3. Lancer FOKARAT
./run.sh

📖 Guide complet : INSTALLATION.md

📋 Prérequis
Composant	Version	Obligatoire
Python	3.8+	✅
Git	Latest	✅
OS	Kali / Ubuntu 22.04+ / Debian 11+ ✅

Metasploit Framework	Latest	⚠️ Recommandé
Mingw-w64	Latest	⚠️ Recommandé
Java (JDK)	11+	⚠️ Pour APK Injector
UPX	Latest	⚠️ Pour compression
Espace disque	2 Go min	—
RAM	2 Go min	—

🎮 Utilisation

./run.sh

Menu interactif avec 35+ options organisées en catégories :

text
▶ PAYLOADS      ▶ LISTENERS     ▶ BADUSB        ▶ ATTAQUES
▶ ÉVASION       ▶ PLUGINS       ▶ RAPPORTS      ▶ SÉCURITÉ
▶ ÉTHIQUE       ▶ DIVERS
📖 Guide détaillé : DOCUMENTATION.md

🏗️ Architecture
text
Fokarat/
├── core/                    # Cœur du framework
│   ├── config.py            # Gestion configuration YAML
│   ├── logger.py            # Logs colorés + JSON
│   ├── database.py          # Base SQLite
│   ├── scope.py             # Validation de scope
│   ├── ethics.py            # Kill switch + audit + dry-run
│   ├── crypto.py            # Chiffrement AES-256-GCM
│   ├── sandbox.py           # Isolation CPU/RAM
│   ├── mitre.py             # Mapping MITRE ATT&CK
│   └── plugin_loader.py     # Chargeur de plugins
│
├── modules/                 # Modules fonctionnels
│   ├── payload_generators/  # Python, C++, MSFVenom
│   ├── listeners/           # ncat, Metasploit
│   ├── injectors/           # BadUSB, encoder, flasher, HTTP
│   ├── android/             # APK Injector
│   ├── persistence/         # WMI
│   └── evasion/             # Padding, obfuscation, UPX, anti-VM, anti-debug
│
├── sdk/                     # SDK plugin
│   └── plugin_base.py       # Classe de base pour plugins
│
├── plugins/                 # Plugins utilisateur
│   ├── hello_world.py
│   └── port_scanner.py
│
├── web/                     # API REST
│   ├── api.py               # FastAPI
│   ├── auth.py              # JWT
│   └── webhooks.py          # SIEM/SOAR
│
├── tests/                   # Tests unitaires (pytest)
│
├── .github/                 # CI/CD + templates
│   ├── workflows/ci.yml
│   └── ISSUE_TEMPLATE/
│
├── main.py                  # Point d'entrée CLI
├── pyproject.toml           # Config build + outils
├── install.sh               # Installation auto
├── run.sh                   # Lancement
├── DOCUMENTATION.md         # Guide complet
├── INSTALLATION.md          # Guide d'install détaillé
├── CONTRIBUTING.md          # Guide de contribution
├── ROADMAP.md               # Roadmap projet
├── CHANGELOG.md             # Historique versions
├── SECURITY.md              # Politique sécurité
├── CODE_OF_CONDUCT.md       # Code de conduite
├── TERMS_OF_USE.md          # Conditions d'utilisation
├── DISCLAIMER.md            # Avertissement légal
└── LICENSE                  # MIT
🧩 Créer un plugin
FOKARAT dispose d'un SDK pour ajouter des modules facilement.

python
# plugins/mon_plugin.py
from sdk import PluginBase, PluginMetadata

class MonPlugin(PluginBase):
    @property
    def metadata(self):
        return PluginMetadata(
            name="Mon Plugin",
            version="1.0.0",
            author="Votre Nom",
            description="Description du plugin",
            category="misc",
            tags=["demo"],
        )

    def run(self, config, args=None):
        print("Hello from my plugin!")
        return {"status": "success"}
Le plugin est automatiquement détecté au prochain lancement de FOKARAT.

📖 Guide complet : CONTRIBUTING.md

📚 Documentation
Fichier	Contenu
DOCUMENTATION.md	Guide complet de tous les modules
INSTALLATION.md	Installation pas à pas + dépendances
CONTRIBUTING.md	Comment contribuer
ROADMAP.md	Feuille de route du projet
CHANGELOG.md	Historique des versions
SECURITY.md	Politique de sécurité
DISCLAIMER.md	Avertissement légal
⚠️ Avertissement légal
FOKARAT est fourni à des fins strictement éducatives et de recherche en sécurité.

✅ Tests sur vos propres systèmes

✅ Formation encadrée

✅ CTF autorisées

✅ Recherche académique

❌ JAMAIS sans autorisation écrite

❌ JAMAIS sur des systèmes tiers

❌ JAMAIS pour des activités illégales

L'auteur décline toute responsabilité en cas d'usage abusif.

📖 Lire l'avertissement complet : DISCLAIMER.md

🗺️ Roadmap
Version	Statut	Description
v1.0	✅	Fondations (payloads, listeners)
v2.0	✅	BadUSB + interface animée
v3.0	✅	Évasion AV + API + SQLite
v3.1	✅	Éthique + scope + kill switch
v3.2	✅	Système de plugins (SDK)
v3.3	✅	MITRE ATT&CK + API stable
v3.4	✅	Crypto AES + sandbox + JWT + webhooks
v3.5	🚧	Tests unitaires + CI/CD complet
v4.0	📅	Interface web + multi-utilisateurs
📖 Roadmap détaillée : ROADMAP.md

🤝 Contribuer
Les contributions sont les bienvenues ! Que ce soit pour :

🐛 Signaler un bug

💡 Proposer une fonctionnalité

📝 Améliorer la documentation

🧩 Créer un plugin

📖 Guide : CONTRIBUTING.md

📜 Licence
Ce projet est sous licence MIT — voir LICENSE.

Vous êtes libre de :

✅ Utiliser commercialement

✅ Modifier

✅ Distribuer

✅ Sublicencier

À condition de conserver la notice de copyright.

🙏 Remerciements
TheFatRat — Inspiration

Metasploit Framework — Payloads

Hak5 — BadUSB

MITRE ATT&CK — Framework de mapping

La communauté open-source

📞 Contact
<div align="center">
Lwano Amissi Blanchard (FOKAS)

📍 Bukavu, RDC 🇨🇩

https://img.shields.io/badge/Email-amissilwano5@gmail.com-red?style=for-the-badge&logo=gmail
https://img.shields.io/badge/GitHub-amissilwano5--beep-black?style=for-the-badge&logo=github
https://img.shields.io/badge/WhatsApp-Cha%C3%AEne-25D366?style=for-the-badge&logo=whatsapp

⭐ Si FOKARAT vous aide, laissez une étoile sur GitHub !

FOKAS — Building the future, one tool at a time.

</div> ```
📄 Fichier 2 : main.py (Version 3.5 — Sans IA)
Efface tout ton main.py et colle ceci :

python
#!/usr/bin/env python3
"""
FOKARAT v3.5 - Framework de cybersécurité
Version sans module IA (allégée)
Auteur: Lwano Amissi Blanchard (FOKAS)
"""
import os
import sys
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import Config
from core.logger import Logger
from core.utils import which
from core.database import Database
from core.scope import ScopeValidator
from core.ethics import EthicsController
from core.plugin_loader import PluginLoader
from core.mitre import MitreMapper
from core.crypto import CryptoManager
from core.sandbox import Sandbox

from modules.payload_generators.python_gen import PythonPayloadGenerator
from modules.payload_generators.cpp_gen import CppPayloadGenerator
from modules.payload_generators.msfvenom_gen import MsfvenomGenerator
from modules.listeners.listener_manager import ListenerManager
from modules.injectors.badusb_gen import BadUSBGenerator
from modules.injectors.duck_encoder import DuckEncoder
from modules.injectors.usb_flasher import USBFlasher
from modules.injectors.http_server import HTTPServer
from modules.android.apk_injector import ApkInjector
from modules.persistence.wmi_persist import WMIPersistence
from modules.evasion.payload_padding import PaddingGenerator
from modules.evasion.python_obfuscator import PythonObfuscator
from modules.evasion.upx_packer import UPXPacker
from modules.evasion.multi_encoder import MultiEncoder
from modules.evasion.anti_vm import AntiVMGenerator
from modules.evasion.anti_debug import AntiDebugGenerator


logger = Logger()
config = Config()
listener = ListenerManager()
http_server = HTTPServer()
db = Database()
scope_validator = ScopeValidator()
ethics = EthicsController()
plugin_loader = PluginLoader()
mitre = MitreMapper()
crypto = CryptoManager()
sandbox = Sandbox()


class C:
    R = "\033[0m"; B = "\033[1m"; D = "\033[2m"
    RED = "\033[91m"; GRN = "\033[92m"; YEL = "\033[93m"
    BLU = "\033[94m"; MAG = "\033[95m"; CYN = "\033[96m"
    WHT = "\033[97m"; PNK = "\033[38;5;213m"


BANNER = f"""{C.GRN}{C.B}
   ███████╗ ██████╗ ██╗  ██╗ █████╗ ██████╗  █████╗ ████████╗
   ██╔════╝██╔═══██╗██║ ██╔╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
   █████╗  ██║   ██║█████╔╝ ███████║██████╔╝███████║   ██║
   ██╔══╝  ██║   ██║██╔═██╗ ██╔══██║██╔══██╗██╔══██║   ██║
   ██║     ╚██████╔╝██║  ██╗██║  ██║██║  ██║██║  ██║   ██║
   ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   {C.R}
{C.CYN}{C.B}              Building the future, one tool at a time.{C.R}
{C.YEL}                    FOKARAT Framework v3.5{C.R}
"""


BOOT_SEQUENCE = [
    ("[BOOT 01] Initialisation du noyau FOKARAT...", 0.06),
    ("[BOOT 02] Chargement des modules payloads...", 0.06),
    ("[BOOT 03] Chargement des listeners...", 0.06),
    ("[BOOT 04] Chargement des modules Android...", 0.06),
    ("[BOOT 05] Chargement des modules d'évasion...", 0.06),
    ("[BOOT 06] Initialisation de la base de données...", 0.06),
    ("[BOOT 07] Chargement du contrôleur éthique...", 0.06),
    ("[BOOT 08] Validation du scope...", 0.06),
    ("[BOOT 09] Chargement du système de plugins...", 0.06),
    ("[BOOT 10] Chargement du mapper MITRE...", 0.06),
    ("[BOOT 11] Initialisation du chiffrement AES...", 0.06),
    ("[BOOT 12] Initialisation du sandbox...", 0.06),
    ("[BOOT 13] Vérification des dépendances...", 0.10),
    ("[BOOT 14] Système prêt pour la session.", 0.20),
]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def typewriter(text, delay=0.008, color=C.WHT):
    for char in text:
        sys.stdout.write(f"{color}{char}{C.R}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def spinner(duration=0.6, message="Chargement", color=C.CYN):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r  {color}{frames[i % len(frames)]}{C.R} {message}...")
        sys.stdout.flush()
        time.sleep(0.06)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 15) + "\r")


def progress_bar(duration=0.8, width=40, color=C.GRN):
    sys.stdout.write("  ")
    for i in range(width + 1):
        pct = int(i / width * 100)
        sys.stdout.write(f"\r  {color}{'█' * i}{C.D}{'░' * (width - i)}{C.R} {C.B}{pct:3d}%{C.R}")
        sys.stdout.flush()
        time.sleep(duration / width)
    print()


def boot_animation():
    clear()
    print()
    for msg, delay in BOOT_SEQUENCE:
        typewriter(f"  {C.YEL}{msg}{C.R}", delay=0.003)
        time.sleep(delay)
    print()
    progress_bar(0.6, 50, C.CYN)
    time.sleep(0.2)


def animated_banner():
    clear()
    print()
    for line in BANNER.split("\n"):
        print(f"  {line}")
        time.sleep(0.015)
    print()


def separator(char="═", length=62, color=C.CYN):
    return f"{color}{char * length}{C.R}"


def menu_option(key, label, color=C.WHT):
    return f"  {C.YEL}│{C.R}  {C.GRN}[{key}]{C.R}  {color}{label}{C.R}"


def show_menu():
    clear()
    animated_banner()

    lhost = config.get("lhost") or f"{C.RED}(non défini){C.R}"
    lport = config.get("lport")
    scope_status = f"{C.GRN}✓{C.R}" if scope_validator.active_scope else f"{C.RED}✗{C.R}"
    dry_status = f"{C.YEL}ON{C.R}" if ethics.dry_run else f"{C.D}OFF{C.R}"
    plugins_count = len(plugin_loader.plugins)
    crypto_backend = crypto.get_backend()

    print(f"  {C.MAG}◆{C.R} LHOST:{C.CYN}{lhost}{C.R}  "
          f"{C.MAG}◆{C.R} LPORT:{C.CYN}{lport}{C.R}  "
          f"{C.MAG}◆{C.R} Scope:{scope_status}  "
          f"{C.MAG}◆{C.R} DRY:{dry_status}  "
          f"{C.MAG}◆{C.R} Plugins:{C.CYN}{plugins_count}{C.R}  "
          f"{C.MAG}◆{C.R} Crypto:{C.CYN}{crypto_backend}{C.R}")
    print()
    print(separator("═", 62, C.CYN))

    print(f"  {C.B}{C.MAG}▶ PAYLOADS{C.R}")
    print(menu_option("01", "Payload Python"))
    print(menu_option("02", "Payload C++ (Mingw)"))
    print(menu_option("03", "Payload MSFVenom"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.MAG}▶ LISTENERS{C.R}")
    print(menu_option("04", "Listener ncat"))
    print(menu_option("05", "Listener Metasploit"))
    print(menu_option("06", "Arrêter tous les listeners", C.RED))
    print(menu_option("07", "Serveur HTTP"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.MAG}▶ BADUSB{C.R}")
    print(menu_option("08", "Générer DuckyScript"))
    print(menu_option("09", "Encoder .duck → .bin"))
    print(menu_option("10", "Flasher USB"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.MAG}▶ ATTAQUES{C.R}")
    print(menu_option("11", "APK Injector (Android)"))
    print(menu_option("12", "Persistance WMI"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.RED}▶ ÉVASION ANTIVIRUS{C.R}")
    print(menu_option("20", "Padding aléatoire (C++)"))
    print(menu_option("21", "Obfuscation Python"))
    print(menu_option("22", "Compression UPX"))
    print(menu_option("23", "Multi-encodage MSFVenom"))
    print(menu_option("24", "Anti-VM"))
    print(menu_option("25", "Anti-Debug"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.PNK}▶ PLUGINS{C.R}")
    print(menu_option("40", f"Lister les plugins ({plugins_count})"))
    print(menu_option("41", "Exécuter un plugin"))
    print(menu_option("42", "Recharger les plugins"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.CYN}▶ RAPPORTS{C.R}")
    print(menu_option("26", "Rapport d'opérations (Markdown)"))
    print(menu_option("33", "Rapport MITRE ATT&CK"))
    print(menu_option("34", "Export MITRE Navigator (JSON)"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.YEL}▶ SÉCURITÉ AVANCÉE{C.R}")
    print(menu_option("50", "Chiffrer un fichier (AES-256)"))
    print(menu_option("51", "Déchiffrer un fichier"))
    print(menu_option("52", "Tester le sandbox (limites)"))
    print(menu_option("53", "Générer un token JWT API"))
    print(menu_option("54", "Ajouter un webhook SIEM"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.RED}▶ ÉTHIQUE & LÉGAL{C.R}")
    print(menu_option("30", "Déclarer un scope"))
    print(menu_option("31", "Activer / Désactiver DRY-RUN"))
    print(menu_option("32", "Journal d'audit"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.MAG}▶ DIVERS{C.R}")
    print(menu_option("14", "Configuration LHOST/LPORT"))
    print(menu_option("15", "Sauvegarder la config"))
    print(menu_option("16", "Ouvrir msfconsole"))
    print(menu_option("17", "Vérifier les dépendances"))
    print(menu_option("27", "Lancer l'API Web (port 5000)"))
    print(menu_option("18", "Crédits"))
    print(menu_option("19", "Quitter", C.RED))

    print(separator("═", 62, C.CYN))
    print()


def check_dependencies():
    clear()
    animated_banner()
    print(f"  {C.B}{C.CYN}═══ DÉPENDANCES ═══{C.R}\n")
    deps = {
        "python3": "Interpréteur Python", "pip": "Gestionnaire Python",
        "git": "Contrôle de version", "g++": "Compilateur C++",
        "x86_64-w64-mingw32-g++": "Compilateur Mingw64",
        "msfvenom": "Générateur Metasploit", "msfconsole": "Console Metasploit",
        "ncat": "Netcat moderne", "apktool": "Décompilation APK",
        "jarsigner": "Signature Java", "zipalign": "Alignement APK",
        "keytool": "Gestion keystore", "java": "Java Runtime",
        "upx": "Compression UPX", "pyinstaller": "Compil Python → exe",
    }
    missing = []
    for cmd, desc in deps.items():
        if which(cmd):
            print(f"  {C.GRN}[✓]{C.R} {C.B}{cmd:<28}{C.R} {C.D}{desc}{C.R}")
        else:
            print(f"  {C.RED}[✗]{C.R} {C.B}{cmd:<28}{C.R} {C.D}{desc}{C.R}")
            missing.append(cmd)
    print()
    if missing:
        logger.warning(f"{len(missing)} outil(s) manquant(s).")
    else:
        logger.success("Toutes les dépendances présentes !")
    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")


# ─── Gestionnaires Évasion ────────────────────────
def handle_padding():
    path = input(f"  {C.YEL}.c à protéger :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Fichier introuvable.")
        return
    with open(path, encoding="utf-8") as f:
        code = f.read()
    out = path.replace(".c", "_protected.c")
    with open(out, "w", encoding="utf-8") as f:
        f.write(PaddingGenerator().wrap_payload(code, 8, 15))
    logger.success(f"Protégé : {out}")
    ethics.audit("PADDING", out)


def handle_python_obfuscation():
    path = input(f"  {C.YEL}.py à obfusquer :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Fichier introuvable.")
        return
    with open(path, encoding="utf-8") as f:
        code = f.read()
    out = path.replace(".py", "_obf.py")
    with open(out, "w", encoding="utf-8") as f:
        f.write(PythonObfuscator().obfuscate(code))
    logger.success(f"Obfusqué : {out}")
    ethics.audit("PY_OBF", out)


def handle_upx():
    path = input(f"  {C.YEL}Binaire :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Introuvable.")
        return
    UPXPacker().pack(path, True)
    ethics.audit("UPX", path)


def handle_multi_encoder():
    MultiEncoder().list_encoders()
    key = input(f"  {C.YEL}Choix [1] :{C.R} ").strip() or "1"
    lhost = input(f"  {C.YEL}LHOST :{C.R} ").strip()
    if not lhost:
        logger.error("LHOST obligatoire.")
        return
    try:
        lport = int(input(f"  {C.YEL}LPORT :{C.R} ").strip())
        iters = int(input(f"  {C.YEL}Itérations [5] :{C.R} ").strip() or "5")
    except ValueError:
        logger.error("Invalide.")
        return
    out = os.path.join(config.get("output_dir", "output"), f"payload_enc_{key}.exe")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    MultiEncoder().encode("windows/meterpreter/reverse_tcp", lhost, lport, out, key, iters)


def handle_anti_vm():
    path = input(f"  {C.YEL}.c :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Introuvable.")
        return
    with open(path) as f:
        code = f.read()
    out = path.replace(".c", "_antivm.c")
    with open(out, "w") as f:
        f.write(AntiVMGenerator().wrap_with_anti_vm(code))
    logger.success(f"Anti-VM : {out}")


def handle_anti_debug():
    path = input(f"  {C.YEL}.c :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Introuvable.")
        return
    with open(path) as f:
        code = f.read()
    out = path.replace(".c", "_antidbg.c")
    with open(out, "w") as f:
        f.write(AntiDebugGenerator().wrap(code))
    logger.success(f"Anti-Debug : {out}")


def handle_report():
    path = db.export_report()
    print(f"\n  {C.GRN}Rapport : {path}{C.R}\n")
    with open(path) as f:
        print(f.read())


def handle_mitre_report():
    audit_file = "output/audit.log"
    if not os.path.exists(audit_file):
        logger.warning("Aucune action enregistrée.")
        return
    action_map = {
        "PADDING_APPLIED": "padding", "PYTHON_OBFUSCATED": "obfuscation",
        "UPX_PACKED": "upx_pack", "MULTI_ENCODED": "multi_encoder",
        "ANTI_VM_APPLIED": "anti_vm", "ANTI_DEBUG_APPLIED": "anti_debug",
        "PAYLOAD_PYTHON": "python_execution", "PAYLOAD_CPP": "cmd_execution",
        "PAYLOAD_MSFVENOM": "reverse_shell", "LISTENER_NCAT": "reverse_shell",
        "LISTENER_MSF": "msf_handler", "BADUSB_GENERATED": "phishing_badusb",
        "WMI_PERSISTENCE": "wmi_persistence", "PLUGIN_EXECUTED": "port_scan",
    }
    actions = set()
    with open(audit_file) as f:
        for line in f:
            try:
                e = json.loads(line)
                if e.get("action") in action_map:
                    actions.add(action_map[e["action"]])
            except Exception:
                pass
    if not actions:
        logger.warning("Aucune action MITRE.")
        return
    content = mitre.generate_report(list(actions))
    out = "output/mitre_report.md"
    os.makedirs("output", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    logger.success(f"Rapport MITRE : {out}")
    print(f"\n{content}\n")


def handle_mitre_navigator():
    audit_file = "output/audit.log"
    if not os.path.exists(audit_file):
        logger.warning("Aucune action.")
        return
    action_map = {
        "PADDING_APPLIED": "padding", "PYTHON_OBFUSCATED": "obfuscation",
        "UPX_PACKED": "upx_pack", "MULTI_ENCODED": "multi_encoder",
        "ANTI_VM_APPLIED": "anti_vm", "ANTI_DEBUG_APPLIED": "anti_debug",
        "PAYLOAD_MSFVENOM": "reverse_shell", "WMI_PERSISTENCE": "wmi_persistence",
    }
    actions = set()
    with open(audit_file) as f:
        for line in f:
            try:
                e = json.loads(line)
                if e.get("action") in action_map:
                    actions.add(action_map[e["action"]])
            except Exception:
                pass
    if not actions:
        logger.warning("Aucune action.")
        return
    out = "output/mitre_navigator.json"
    os.makedirs("output", exist_ok=True)
    mitre.export_navigator_json(list(actions), out)


def handle_web_api():
    logger.info("API sur http://localhost:5000/docs")
    logger.info("Auth : FOKARAT_API_USER / FOKARAT_API_PASS (défaut admin/fokarat)")
    ethics.audit("API_STARTED", "5000")
    try:
        from web.api import start_web
        start_web(host="127.0.0.1", port=5000)
    except ImportError:
        logger.error("pip install fastapi uvicorn")


def handle_scope():
    clear()
    existing = scope_validator.load_scope()
    if existing:
        print(f"  {C.YEL}Scope actif : {existing['target']}{C.R}")
        if input(f"  {C.YEL}Remplacer ? (o/n) :{C.R} ").strip().lower() != "o":
            return
    scope_validator.require_scope()


def handle_dry_run():
    if ethics.dry_run:
        ethics.disable_dry_run()
    else:
        ethics.enable_dry_run()


def handle_audit_log():
    clear()
    print(f"\n  {C.B}{C.CYN}═══ AUDIT ═══{C.R}\n")
    audit_file = "output/audit.log"
    if not os.path.exists(audit_file):
        logger.info("Aucun log.")
        return
    with open(audit_file) as f:
        lines = f.readlines()
    print(f"  {C.D}{len(lines)} entrée(s){C.R}\n")
    for line in lines[-30:]:
        try:
            e = json.loads(line)
            print(f"  [{e['timestamp'][:19]}] {e['action']} : {e.get('details', '')}")
        except Exception:
            pass


def handle_list_plugins():
    clear()
    print(f"\n  {C.B}{C.PNK}═══ PLUGINS ═══{C.R}\n")
    plugins = plugin_loader.list_plugins()
    if not plugins:
        logger.info("Aucun plugin.")
        return
    for i, p in enumerate(plugins, 1):
        m = p.metadata
        print(f"  {C.CYN}[{i}]{C.R} {C.B}{m.name}{C.R} v{m.version} ({m.category})")
        print(f"      {C.D}{m.description}{C.R}\n")


def handle_run_plugin():
    plugins = plugin_loader.list_plugins()
    if not plugins:
        logger.info("Aucun plugin.")
        return
    for i, p in enumerate(plugins, 1):
        print(f"    [{i}] {p.metadata.name}")
    try:
        c = int(input(f"  {C.YEL}Choix :{C.R} ").strip())
        plugin = plugins[c - 1]
    except (ValueError, IndexError):
        logger.error("Invalide.")
        return
    if plugin.metadata.requires_scope and not scope_validator.active_scope:
        if not scope_validator.require_scope():
            return
    if not ethics.confirm_action(f"Exécuter {plugin.metadata.name}"):
        return
    try:
        result = plugin.run(config)
        logger.success(f"Résultat : {result}")
        ethics.audit("PLUGIN_EXECUTED", plugin.metadata.name)
    except Exception as e:
        logger.error(f"Erreur : {e}")


def handle_reload_plugins():
    plugin_loader.unload_all()
    n = plugin_loader.load_all()
    logger.success(f"{n} plugin(s) rechargé(s)")


# ─── Gestionnaires Sécurité ───────────────────────
def handle_encrypt_file():
    path = input(f"  {C.YEL}Fichier à chiffrer :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Introuvable.")
        return
    crypto.encrypt_file(path)
    ethics.audit("FILE_ENCRYPTED", path)


def handle_decrypt_file():
    path = input(f"  {C.YEL}Fichier .enc à déchiffrer :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Introuvable.")
        return
    try:
        content = crypto.decrypt_file(path)
        out = path.replace(".enc", ".dec")
        with open(out, "w", encoding="utf-8") as f:
            f.write(content)
        logger.success(f"Déchiffré : {out}")
        ethics.audit("FILE_DECRYPTED", path)
    except Exception as e:
        logger.error(f"Échec : {e}")


def handle_test_sandbox():
    print(f"\n  {C.YEL}Test du sandbox :{C.R}")
    print(f"  Limites actuelles :")
    for k, v in sandbox.limits.items():
        print(f"    {k} = {v}")
    print()

    cmd = input(f"  {C.YEL}Commande à tester [{C.D}echo hello{C.R}] :{C.R} ").strip()
    if not cmd:
        cmd = "echo hello"

    print()
    result = sandbox.run(cmd)
    print(f"\n  {C.GRN}Status :{C.R} {result['status']}")
    print(f"  {C.GRN}Durée  :{C.R} {result['duration']}s")
    print(f"  {C.GRN}Code   :{C.R} {result['returncode']}")
    if result["stdout"]:
        print(f"  {C.GRN}Sortie :{C.R}\n{result['stdout'][:500]}")
    if result["stderr"]:
        print(f"  {C.YEL}Erreurs :{C.R}\n{result['stderr'][:500]}")

    ethics.audit("SANDBOX_TEST", cmd)


def handle_jwt_token():
    try:
        from web.auth import jwt_manager
        user = input(f"  {C.YEL}Username [admin] :{C.R} ").strip() or "admin"
        token = jwt_manager.create_token(user, expiry=3600)
        print(f"\n  {C.GRN}Token JWT (valide 1h) :{C.R}\n")
        print(f"  {C.CYN}{token}{C.R}\n")
        print(f"  {C.D}Utilisation : Authorization: Bearer <token>{C.R}")
        print(f"  {C.D}Test : curl -H 'Authorization: Bearer {token[:20]}...' http://localhost:5000/payloads{C.R}\n")
        ethics.audit("JWT_GENERATED", user)
    except ImportError as e:
        logger.error(f"Module auth indisponible : {e}")


def handle_webhook_add():
    try:
        from web.webhooks import webhook_manager
        url = input(f"  {C.YEL}URL du webhook (Slack, Splunk, etc.) :{C.R} ").strip()
        if not url:
            return
        webhook_manager.add_hook(url)
        ethics.audit("WEBHOOK_ADDED", url)
        print(f"\n  {C.GRN}Webhook ajouté. Il recevra tous les événements.{C.R}\n")
    except ImportError as e:
        logger.error(f"Module webhooks indisponible : {e}")


def main():
    boot_animation()
    time.sleep(0.3)
    scope_validator.load_scope()
    plugin_loader.load_all()

    while True:
        show_menu()
        choice = input(f"  {C.B}{C.MAG}╰─▶{C.R} {C.B}FOKARAT{C.R} {C.YEL}>{C.R} ").strip()

        try:
            if choice == "01":
                if ethics.confirm_action("Payload Python"):
                    PythonPayloadGenerator().run(config)
            elif choice == "02":
                if ethics.confirm_action("Payload C++"):
                    CppPayloadGenerator().run(config)
            elif choice == "03":
                if ethics.confirm_action("Payload MSFVenom"):
                    MsfvenomGenerator().run(config)
            elif choice == "04":
                listener.start_ncat(config)
            elif choice == "05":
                listener.start_msf(config)
            elif choice == "06":
                listener.stop_all()
            elif choice == "07":
                http_server.run(config); continue
            elif choice == "08":
                if ethics.confirm_action("DuckyScript"):
                    BadUSBGenerator().run(config)
            elif choice == "09":
                DuckEncoder().run(config)
            elif choice == "10":
                if ethics.confirm_action("Flash USB"):
                    USBFlasher().run(config)
            elif choice == "11":
                if ethics.confirm_action("APK Injector"):
                    ApkInjector().run(config)
            elif choice == "12":
                if ethics.confirm_action("WMI"):
                    WMIPersistence().run(config)
            elif choice == "14":
                ip = input(f"  LHOST [{config.get('lhost')}] : ").strip()
                if ip: config.set("lhost", ip)
                p = input(f"  LPORT [{config.get('lport')}] : ").strip()
                if p.isdigit(): config.set("lport", int(p))
                logger.success("Config mise à jour.")
            elif choice == "15":
                if config.save(): logger.success("Sauvegardée.")
            elif choice == "16":
                if which("msfconsole"): os.system("msfconsole")
                else: logger.error("msfconsole absent.")
            elif choice == "17":
                check_dependencies(); continue
            elif choice == "18":
                clear(); animated_banner()
                print(f"  {C.B}{C.GRN}FOKARAT v3.5{C.R}")
                print(f"  Auteur : Lwano Amissi Blanchard (FOKAS)")
                print(f"  Bukavu, RDC — Usage éducatif uniquement.\n")
            elif choice == "19":
                listener.stop_all(); plugin_loader.unload_all()
                typewriter(f"\n  {C.GRN}À bientôt !{C.R}", 0.02); print(); break

            elif choice == "20": handle_padding()
            elif choice == "21": handle_python_obfuscation()
            elif choice == "22": handle_upx()
            elif choice == "23": handle_multi_encoder()
            elif choice == "24": handle_anti_vm()
            elif choice == "25": handle_anti_debug()
            elif choice == "26": handle_report()
            elif choice == "27": handle_web_api(); continue

            elif choice == "30": handle_scope()
            elif choice == "31": handle_dry_run()
            elif choice == "32": handle_audit_log()

            elif choice == "33": handle_mitre_report()
            elif choice == "34": handle_mitre_navigator()

            elif choice == "40": handle_list_plugins()
            elif choice == "41": handle_run_plugin()
            elif choice == "42": handle_reload_plugins()

            elif choice == "50": handle_encrypt_file()
            elif choice == "51": handle_decrypt_file()
            elif choice == "52": handle_test_sandbox()
            elif choice == "53": handle_jwt_token()
            elif choice == "54": handle_webhook_add()

            else:
                logger.warning("Choix invalide.")

        except KeyboardInterrupt:
            print(); logger.warning("Interrompu.")
        except Exception as e:
            logger.error(f"Erreur : {e}")

        input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        listener.stop_all()
        plugin_loader.unload_all()
        print(f"\n{C.RED}[!] Sortie.{C.R}")
🗑️ Supprimer aussi le dossier ai/ (optionnel)
bash
cd ~/Bureau/Fokarat
rm -rf ai/
Le dossier ai/ n'est plus utilisé. Tu peux le supprimer.

Si tu veux le garder mais inactif, laisse-le, aucun import ne le charge plus.

⚠️ Mise à jour du pyproject.toml
Le pyproject.toml référence encore "ai" dans les packages. Il faut retirer cette ligne.

Efface pyproject.toml et colle ceci :

toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "fokarat"
version = "3.5.0"
description = "Framework de cybersécurité éducatif - Building the future, one tool at a time"
readme = "README.md"
license = { text = "MIT" }
authors = [
    { name = "Lwano Amissi Blanchard (FOKAS)", email = "amissilwano5@gmail.com" }
]
requires-python = ">=3.8"
keywords = ["cybersecurity", "framework", "pentest", "education", "python"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Intended Audience :: Information Technology",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Security",
    "Operating System :: POSIX :: Linux",
]

dependencies = [
    "pyyaml>=6.0",
    "requests>=2.31.0",
    "customtkinter>=5.2.0",
    "Pillow>=10.0.0",
    "psutil>=5.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
    "ruff>=0.1.0",
    "black>=23.10.0",
    "mypy>=1.6.0",
    "pre-commit>=3.5.0",
    "bandit>=1.7.5",
]
web = ["fastapi>=0.104.0", "uvicorn>=0.24.0"]
build = ["pyinstaller>=6.0.0"]
all = ["fastapi>=0.104.0", "uvicorn>=0.24.0", "pyinstaller>=6.0.0"]

[project.urls]
Homepage = "https://github.com/amissilwano5-beep/Fokarat"
Repository = "https://github.com/amissilwano5-beep/Fokarat"
Issues = "https://github.com/amissilwano5-beep/Fokarat/issues"
Documentation = "https://github.com/amissilwano5-beep/Fokarat/blob/main/DOCUMENTATION.md"
Changelog = "https://github.com/amissilwano5-beep/Fokarat/blob/main/CHANGELOG.md"

[project.scripts]
fokarat = "main:main"

[tool.setuptools]
packages = ["core", "modules", "web"]
py-modules = ["main", "gui"]

[tool.ruff]
line-length = 100
target-version = "py38"
src = ["."]
exclude = [".git", ".venv", "venv", "__pycache__", "output", "tools", "build", "dist"]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "UP", "B", "C4", "SIM", "RUF"]
ignore = ["E501", "B008", "RUF001", "RUF002", "RUF003"]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]
"__init__.py" = ["F401"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.black]
line-length = 100
target-version = ["py38", "py39", "py310", "py311", "py312"]
extend-exclude = '''
/(\.git|\.venv|venv|__pycache__|output|tools|build|dist)/
'''

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
check_untyped_defs = true
no_implicit_optional = true
show_error_codes = true
exclude = ["output", "tools", "build", "dist", ".venv", "venv"]

[[tool.mypy.overrides]]
module = ["customtkinter.*", "duckencoder.*"]
ignore_missing_imports = true

[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = ["-v", "--strict-markers", "--tb=short"]
markers = [
    "slow: tests lents",
    "network: tests nécessitant un accès réseau",
    "integration: tests d'intégration",
]

[tool.coverage.run]
source = ["core", "modules"]
omit = ["*/tests/*", "*/test_*.py", "*/__init__.py", "*/output/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if __name__ == .__main__.:",
    "@abstractmethod",
]

[tool.bandit]
exclude_dirs = ["tests", "output", "tools", "build", "dist"]
skips = ["B101", "B601"]
