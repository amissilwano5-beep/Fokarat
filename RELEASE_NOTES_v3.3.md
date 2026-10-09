# 🚀 FOKARAT v3.4 — Release Notes

**Date** : Octobre 2026
**Auteur** : Lwano Amissi Blanchard (FOKAS)
**License** : MIT

---

## 🎉 Nouveautés

### 🔐 Sécurité avancée
- **Chiffrement AES-256-GCM** des secrets (`core/crypto.py`)
- **Sandbox d'exécution** avec limites CPU/RAM/temps (`core/sandbox.py`)
- **Authentification JWT** pour l'API (`web/auth.py`)
- **Webhooks SIEM/SOAR** (Slack, Splunk, Elastic) (`web/webhooks.py`)

### 🎯 API REST stable v1.1
- Authentification JWT obligatoire (sauf `/`, `/health`, `/version`)
- Host par défaut `127.0.0.1` (sécurité)
- Nouveaux endpoints : `/auth/token`, `/webhooks/add`, `/webhooks/list`

### 📊 Rapports MITRE ATT&CK
- Mapping automatique des actions
- Export navigateur MITRE JSON

### 🧩 Architecture plugins
- SDK `PluginBase` (`sdk/plugin_base.py`)
- PluginLoader dynamique (`core/plugin_loader.py`)
- Exemples : `hello_world.py`, `port_scanner.py`

### ⚖️ Éthique et légal
- Scope obligatoire avant chaque attaque
- Kill switch (Ctrl+C)
- Mode DRY-RUN
- Journal d'audit JSON

---

## 📦 Nouveaux fichiers

| Catégorie | Fichier |
|-----------|---------|
| Crypto | `core/crypto.py` |
| Sandbox | `core/sandbox.py` |
| MITRE | `core/mitre.py` |
| Plugins | `sdk/plugin_base.py`, `core/plugin_loader.py` |
| Auth | `web/auth.py` |
| Webhooks | `web/webhooks.py` |
| Éthique | `core/scope.py`, `core/ethics.py` |
| Docs | `CONTRIBUTING.md`, `ROADMAP.md`, `INSTALLATION.md` |
| CI/CD | `.github/workflows/ci.yml`, `.github/ISSUE_TEMPLATE/*` |

---

## 🚀 Installation

```bash
git clone https://github.com/amissilwano5-beep/Fokarat.git
cd Fokarat
chmod +x install.sh run.sh
./install.sh
./run.sh