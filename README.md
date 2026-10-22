
'''

## 📄 Fichier 2 : `README.md` (Version 4.0)


```markdown
<div align="center">

# 🛡️ FOKARAT

**Framework de cybersécurité modulaire et éducatif**

[![Version](https://img.shields.io/badge/version-4.0.0-brightgreen.svg?style=for-the-badge)](https://github.com/amissilwano5-beep/Fokarat/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Linux-orange.svg?style=for-the-badge&logo=linux&logoColor=white)](https://www.kali.org/)
[![Made in RDC](https://img.shields.io/badge/Made%20in-RDC%20🇨🇩-yellow.svg?style=for-the-badge)]()

**Building the future, one tool at a time.**

[Documentation](DOCUMENTATION.md) • [Installation](INSTALLATION.md) • [Roadmap](ROADMAP.md) • [Contribuer](CONTRIBUTING.md)

</div>

---

## 🎯 Qu'est-ce que FOKARAT ?

**FOKARAT** est un **framework de cybersécurité éducatif** développé depuis Bukavu (RDC) par [Lwano Amissi Blanchard (FOKAS)](https://github.com/amissilwano5-beep).

Inspiré de **TheFatRat** mais avec une **architecture moderne** : plugins, API REST, MITRE ATT&CK, C2 HTTP(S) chiffré, post-exploitation multi-OS (Windows, Linux, Android, iOS), rapports PDF professionnels.

> ⚠️ **Usage éducatif et tests autorisés uniquement.** Lisez [DISCLAIMER.md](DISCLAIMER.md) avant utilisation.

---

## ✨ Fonctionnalités

### 🎯 Génération de payloads (v1.0)
- **Python** reverse shell (reconnexion auto)
- **C++** cross-platform via Mingw
- **MSFVenom** (8 types)

### 💾 BadUSB (v2.0)
- 5 types d'attaques + contournement UAC via fodhelper
- Support Digispark, Raspberry Pi Pico, Rubber Ducky
- Layouts clavier (QWERTY / AZERTY / QWERTZ)

### 🛡️ Évasion antivirus (v3.0)
- Padding aléatoire (16 Ko + 15 fonctions fake)
- Obfuscation Python multi-couches
- Compression UPX ultra-brute
- Multi-encodage MSFVenom (7 encodeurs)
- Anti-VM (6 méthodes) + Anti-Debug (5 méthodes)

### ⚖️ Éthique & légal (v3.1)
- Scope obligatoire avant chaque action
- Kill switch + mode DRY-RUN
- Journal d'audit JSON

### 🧩 Plugins SDK (v3.2)
- Ajout de modules sans toucher au core
- PluginLoader automatique

### 📊 MITRE ATT&CK (v3.3)
- Mapping automatique des actions
- Export MITRE Navigator (JSON)

### 🔐 Sécurité avancée (v3.4)
- Chiffrement AES-256-GCM des secrets
- Sandbox (limites CPU/RAM/temps)
- Auth JWT pour l'API
- Webhooks SIEM/SOAR

### 🖥️ Post-exploitation Windows (v3.6)
- Énumération complète
- LSASS dump (5 méthodes)
- Persistance (7 techniques)
- AMSI Bypass (5 techniques)
- Mouvement latéral (6 méthodes : psexec, wmiexec, smbexec, winrm, PTH, RDP)

### 🐧 Post-exploitation Linux (v3.7)
- Énumération complète
- Privesc (10 techniques : sudo, SUID, capabilities, cron, docker...)
- Persistance (6 techniques)
- Credentials (7 catégories)
- Mouvement latéral (6 méthodes)

### 🌐 C2 HTTP(S) chiffré (v3.8)
- Serveur C2 avec AES-256-GCM
- Agents Python + PowerShell
- Gestion multi-sessions
- Pivoting (8 méthodes : SSH SOCKS, Chisel, Ligolo, Socat...)

### 📱 Post-exploitation Mobile (v3.9)
- **Android** : enum, persistence (7 tech), credentials, privesc, exfiltration
- **iOS** : enum, jailbreak (5 méthodes), persistence, credentials

### 📄 Rapports PDF pro (v4.0)
- Executive Summary
- Findings avec CVSS v3.1 (12 presets)
- Recommandations globales
- Fallback HTML si reportlab absent

---

## 🚀 Installation rapide

```bash
git clone https://github.com/amissilwano5-beep/Fokarat.git
cd Fokarat
chmod +x install.sh run.sh
./install.sh
./run.sh

📖 Guide complet : INSTALLATION.md

🎮 Utilisation
Menu interactif avec 120+ options organisées par catégories :

text
▶ PAYLOADS          ▶ LISTENERS / BADUSB    ▶ ÉVASION
▶ POST-EXP WINDOWS  ▶ POST-EXP LINUX        ▶ C2
▶ POST-EXP MOBILE   ▶ RAPPORTS PDF          ▶ PLUGINS
▶ SÉCURITÉ          ▶ ÉTHIQUE & LÉGAL       ▶ DIVERS
📖 Guide détaillé : DOCUMENTATION.md

🏗️ Architecture
Fokarat/
├── core/                       # Cœur (config, logger, db, scope, ethics, crypto, sandbox, mitre)
├── modules/
│   ├── payload_generators/    # Python, C++, MSFVenom
│   ├── listeners/             # ncat, Metasploit
│   ├── injectors/             # BadUSB, HTTP server
│   ├── android/               # APK Injector
│   ├── persistence/           # WMI
│   ├── evasion/               # Padding, obfuscation, UPX, anti-VM, anti-debug
│   ├── post_exploitation/
│   │   ├── windows/           # Enum, LSASS, persistence, AMSI, lateral
│   │   ├── linux/             # Enum, privesc, persistence, creds, lateral
│   │   ├── android/           # Enum, persistence, creds, privesc, exfil
│   │   └── ios/               # Enum, jailbreak, persistence, creds
│   ├── c2/                    # C2 HTTP(S), sessions, pivoting, crypto
│   └── reporting/             # CVSS, findings, PDF generator
├── sdk/                       # Plugin SDK
├── plugins/                   # Plugins utilisateur
├── web/                       # API REST (FastAPI)
├── tests/                     # Tests pytest
├── main.py                    # Point d'entrée
├── install.sh / run.sh
└── pyproject.toml

🗺️ Roadmap
Version	Statut	Description
v1.0 - v2.0	✅	Payloads + BadUSB
v3.0 - v3.4	✅	Évasion + Éthique + Plugins + MITRE + Sécurité
v3.6 - v3.7	✅	Post-exploitation Windows + Linux
v3.8 - v3.9	✅	C2 + Mobile
v4.0	✅	Rapports PDF professionnels
4.1	🚧	Tests unitaires + CI/CD complet
v5.0	📅	Interface Web + multi-utilisateurs

📖 ROADMAP.md

📜 Licence
MIT — voir LICENSE.

⚠️ Avertissement légal
Usage éducatif et tests autorisés uniquement. Voir DISCLAIMER.md.

📞 Contact
<div align="center">
Lwano Amissi Blanchard (FOKAS)
📍 Bukavu, RDC 🇨🇩

https://img.shields.io/badge/Email-amissilwano5@gmail.com-red?style=for-the-badge&logo=gmail
https://img.shields.io/badge/GitHub-amissilwano5--beep-black?style=for-the-badge&logo=github

⭐ Si FOKARAT vous aide, laissez une étoile !

FOKAS — Building the future, one tool at a time.
</div> ```
