# 🚀 FOKARAT v4.0.0 — Release Notes

**Date** : 16 octobre 2026
**Auteur** : Lwano Amissi Blanchard (FOKAS)
**License** : MIT

---

## 🎉 Nouveauté majeure

**FOKARAT est maintenant un framework complet** couvrant :
- 🔴 Red team : payloads, évasion AV, C2, post-exploitation
- 🔵 Blue team : MITRE ATT&CK, rapports professionnels, audit
- 📱 Mobile : Android + iOS
- 🖥️ Multi-OS : Windows, Linux, macOS
- 🌐 Multi-canal : CLI + API REST + Plugins

---

## ✨ Ce qui est nouveau dans v4.0

### 📄 Rapports PDF professionnels
- Calculateur **CVSS v3.1** complet
- **Executive Summary** pour le management
- **Findings détaillés** avec preuves, recommandations, références
- **Recommandations globales** basées sur les findings
- Export **Markdown** + **PDF** + **HTML** (fallback)

### 📱 Post-exploitation Mobile
- **Android** : 5 modules (enum, persistence, credentials, privesc, exfiltration)
- **iOS** : 4 modules (enum, jailbreak, persistence, credentials)
- Guides intégrés pour les 5 méthodes de jailbreak

### 🌐 C2 moderne
- Serveur HTTP(S) avec **chiffrement AES-256-GCM**
- Agents **Python** + **PowerShell**
- Gestion **multi-sessions** avec historique
- **8 méthodes de pivoting** (SSH SOCKS, Chisel, Ligolo, Socat...)

---

## 📊 Statistiques v4.0

| Métrique | Valeur |
|----------|--------|
| Options menu | 120+ |
| Modules | 40+ |
| Lignes de code | ~15 000 |
| Catégories MITRE couvertes | 12 |
| OS supportés (post-expl) | Windows, Linux, Android, iOS |
| Méthodes de pivoting | 8 |
| Techniques de persistence | 18 (7+6+5) |

---

## ⚠️ Avertissement légal

FOKARAT est fourni à des fins **strictement éducatives** et de **recherche en sécurité**.

Utilisez-le uniquement sur :
- ✅ Vos propres systèmes
- ✅ Des labs isolés
- ✅ Des tests autorisés par écrit

**Jamais** sur des systèmes tiers sans autorisation.

---

## 📦 Installation

```bash
git clone https://github.com/amissilwano5-beep/Fokarat.git
cd Fokarat
chmod +x install.sh run.sh
./install.sh
./run.sh

Guide complet : INSTALLATION.md

🔗 Liens
Repo : https://github.com/amissilwano5-beep/Fokarat

Issues : https://github.com/amissilwano5-beep/Fokarat/issues

Discussions : https://github.com/amissilwano5-beep/Fokarat/discussions

Email : amissilwano5@gmail.com

FOKAS — Building the future, one tool at a time.

