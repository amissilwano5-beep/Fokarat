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


