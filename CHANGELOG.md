# Changelog

Toutes les modifications notables de FOKARAT sont documentées dans ce fichier.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)
et le versionnage sémantique [SemVer](https://semver.org/lang/fr/).

## [3.0.0] - 2026-10-07

### Ajouté
- 🛡️ Modules d'évasion antivirus :
  - Padding aléatoire C++ (`payload_padding.py`)
  - Obfuscation Python multi-couches (`python_obfuscator.py`)
  - Compression UPX (`upx_packer.py`)
  - Multi-encodage MSFVenom (`multi_encoder.py`)
  - Protection Anti-VM (`anti_vm.py`)
  - Protection Anti-Debug (`anti_debug.py`)
- 🗄️ Base de données SQLite (`core/database.py`)
- 🌐 API REST FastAPI (`web/api.py`)
- 📊 Rapport d'opérations automatique
- 🎨 Interface animée avec boot sequence
- 📖 Documentation complète (`DOCUMENTATION.md`)

### Modifié
- Interface principale (`main.py`) - 27 options au total
- Menu réorganisé en sections colorées

## [2.0.0] - 2026-10-06

### Ajouté
- 🎨 Interface animée (spinner, progress bar, typewriter)
- 💾 Module BadUSB complet (5 types d'attaques)
- 🔐 Encodeur DuckyScript (`duck_encoder.py`)
- 🔌 Flasher USB (`usb_flasher.py`)
- 🌐 Serveur HTTP local (`http_server.py`)
- 📱 APK Injector (`apk_injector.py`)
- 📖 Documentation complète

## [1.0.0] - 2026-10-05

### Ajouté
- 🚀 Version initiale
- Générateurs Python/C++/MSFVenom
- Listeners ncat/Metasploit
- Menu CLI basique