# Changelog

Toutes les modifications notables de FOKARAT sont documentées ici.

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)
Versionnage : [SemVer](https://semver.org/lang/fr/)

## [4.0.0] - 2026-10-16

### Ajouté
- 📄 **Rapports PDF professionnels** (`modules/reporting/`)
  - Calculateur CVSS v3.1 complet + 12 presets
  - Gestionnaire de findings (CRUD + JSON)
  - Rapport PDF (couverture, exec summary, findings, recommandations)
  - Executive Summary Markdown
  - Fallback HTML si reportlab absent
- 📱 **Post-exploitation Android** (`modules/post_exploitation/android/`)
  - Énumération (10 sections)
  - Persistance (7 techniques)
  - Credentials (9 catégories)
  - Privesc (7 techniques)
  - Exfiltration (5 méthodes)
- 🍎 **Post-exploitation iOS** (`modules/post_exploitation/ios/`)
  - Énumération (10 sections)
  - Jailbreak (détection + guide de 5 méthodes)
  - Persistance (5 techniques)
  - Credentials (9 catégories)
- 🌐 **C2 HTTP(S) chiffré** (`modules/c2/`)
  - Serveur C2 + agent Python/PowerShell
  - Chiffrement AES-256-GCM
  - Gestion multi-sessions
  - Pivoting (8 méthodes)
- 🐧 **Post-exploitation Linux** (`modules/post_exploitation/linux/`)
  - Énumération, privesc (10 tech), persistence (6 tech), credentials, lateral (6)
- 🖥️ **Post-exploitation Windows** (`modules/post_exploitation/windows/`)
  - Énumération, LSASS dump, persistence (7 tech), AMSI bypass, lateral (6)
- 📊 Mapping MITRE ATT&CK étendu

### Modifié
- Menu principal : 120+ options organisées en 12 catégories
- Version 3.9 → 4.0

## [3.5.1] - 2026-10-10

### Corrigé (critique)
- **Scope appliqué partout** : PluginBase.run() vérifie le scope si requires_scope=True
- **API sécurisée** : refuse de démarrer sans FOKARAT_API_USER/PASS
- **Plugins non-interactifs** : args au lieu de input()
- **Dépendances** : fastapi, uvicorn, python-jose ajoutés
- **pyproject.toml** : complet et installable
- Code mort supprimé dans port_scanner.py

## [3.5.0] - 2026-10-07

### Ajouté
- Chiffrement AES-256-GCM (`core/crypto.py`)
- Sandbox avec limites CPU/RAM (`core/sandbox.py`)
- API JWT (`web/auth.py`)
- Webhooks SIEM/SOAR (`web/webhooks.py`)

### Supprimé
- Module IA local (trop lourd)

## [3.4.0] - 2026-10-06

### Ajouté
- Chiffrement AES + sandbox
- Auth JWT API v1.1
- Webhooks SIEM

## [3.3.0] - 2026-10-05

### Ajouté
- MITRE ATT&CK mapping
- Export MITRE Navigator
- API REST stable

## [3.2.0] - 2026-10-05

### Ajouté
- SDK PluginBase + PluginLoader
- Exemples de plugins

## [3.1.0] - 2026-10-04

### Ajouté
- Scope obligatoire
- Kill switch
- Journal d'audit
- Fichiers légaux (LICENSE, SECURITY, CODE_OF_CONDUCT, TERMS)

## [3.0.0] - 2026-10-04

### Ajouté
- Modules d'évasion (padding, obfuscation, UPX, multi-encoder, anti-VM, anti-debug)
- Base SQLite
- API Web basique
- Interface animée

## [2.0.0] - 2026-10-03

### Ajouté
- BadUSB complet (5 types d'attaques)
- Encodeur DuckyScript
- Flasher USB
- Serveur HTTP
- APK Injector

## [1.0.0] - 2026-10-01

### Ajouté
- Générateurs de payloads (Python, C++, MSFVenom)
- Listeners (ncat, Metasploit)
- Menu CLI