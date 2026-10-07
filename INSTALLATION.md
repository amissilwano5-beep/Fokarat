# 📦 FOKARAT - Guide d'Installation Complet

**Dernière mise à jour : Octobre 2026**

Ce document liste TOUT ce qu'il faut installer pour que FOKARAT fonctionne à 100%.

---

## 🎯 État actuel (Octobre 2026)

À ce jour, **FOKARAT fonctionne à 70%** sans rien installer de plus.
Les options qui fonctionnent **immédiatement** :

| Option | Fonctionne sans install |
|--------|------------------------|
| 01 | ✅ Payload Python (si `python3`) |
| 02 | ❌ Nécessite `mingw-w64` |
| 03 | ❌ Nécessite `msfvenom` |
| 04 | ❌ Nécessite `ncat` |
| 05 | ❌ Nécessite `msfconsole` |
| 06-07 | ✅ |
| 08-09 | ⚠️ Partial (encoder à télécharger) |
| 10 | ❌ Nécessite matériel USB |
| 11 | ❌ Nécessite `apktool` + `jarsigner` |
| 12 | ✅ (script généré) |
| 13 | ⚠️ Nécessite `llama-cpp-python` + modèle |
| 14-19 | ✅ |
| 20-25 | ✅ |
| 26 | ✅ |
| 27 | ❌ Nécessite `fastapi` + `uvicorn` |
| 30-32 | ✅ |
| 33-34 | ✅ |
| 40-42 | ✅ |

---

## 📋 LISTE COMPLÈTE DES INSTALLATIONS

### 🔧 ÉTAPE 1 : Outils système (APT)

```bash
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    g++ \
    make \
    build-essential

Taille : ~200 Mo
Obligatoire : OUI

🔧 ÉTAPE 2 : Outils cybersécurité (APT)
bash
sudo apt install -y \
    mingw-w64 \
    ncat \
    metasploit-framework \
    apktool \
    default-jdk \
    zipalign \
    upx-ucl \
    binutils-avr

Taille : ~500 Mo (Metasploit est gros)
Obligatoire : Recommandé

Ce que ça débloque :

Outil	Options débloquées
mingw-w64	[02] Payload C++ Windows
ncat	[04] Listener ncat
metasploit-framework	[03], [05], [16] MSFVenom + Handler + msfconsole
apktool + default-jdk + zipalign	[11] APK Injector
upx-ucl	[22] Compression UPX
binutils-avr	[10] Flash Digispark
🔧 ÉTAPE 3 : Environnement virtuel Python
bash
cd ~/Bureau/Fokarat
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
Obligatoire : OUI

🔧 ÉTAPE 4 : Dépendances Python (base)
bash
pip install -r requirements.txt
Ou manuellement :

bash
pip install \
    pyyaml \
    requests \
    customtkinter \
    Pillow \
    psutil
Taille : ~50 Mo
Obligatoire : OUI

🔧 ÉTAPE 5 : Dépendances Python (développement)
bash
pip install \
    pytest \
    pytest-cov \
    pytest-mock \
    ruff \
    black \
    mypy \
    pre-commit \
    bandit
Taille : ~200 Mo
Obligatoire : NON (pour tests et qualité)

Ce que ça débloque :

pytest : tests unitaires

ruff : linter rapide

black : formateur

mypy : vérification de types

pre-commit : hooks Git

bandit : scan de sécurité

🔧 ÉTAPE 6 : Dépendances Python (optionnelles)
bash
# API REST
pip install fastapi uvicorn

# Compilation .exe
pip install pyinstaller

# IA locale (⚠️ ~50 Mo)
pip install llama-cpp-python
Taille : ~100 Mo (sans modèle IA)
Obligatoire : NON

Ce que ça débloque :

Package	Options
fastapi + uvicorn	[27] API Web
pyinstaller	Compilation Python → exe
llama-cpp-python	[13] Assistant IA (nécessite un modèle GGUF ~4-8 Go en plus)
🚀 INSTALLATION AUTOMATIQUE (tout-en-un)
Crée un fichier setup_all.sh avec ce contenu :

bash
#!/bin/bash
# FOKARAT - Installation complète
set -e

echo "════════════════════════════════════════"
echo "  FOKARAT - Installation complète"
echo "════════════════════════════════════════"

# 1. Outils système
echo ""
echo "[1/5] Outils système (apt)..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git g++ make build-essential

# 2. Outils cybersécurité
echo ""
echo "[2/5] Outils cybersécurité (apt)..."
sudo apt install -y mingw-w64 ncat metasploit-framework apktool \
    default-jdk zipalign upx-ucl binutils-avr

# 3. Environnement virtuel
echo ""
echo "[3/5] Environnement virtuel Python..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# 4. Dépendances Python
echo ""
echo "[4/5] Dépendances Python..."
pip install -r requirements.txt 2>/dev/null || \
    pip install pyyaml requests customtkinter Pillow psutil

# 5. Dev + Options
echo ""
echo "[5/5] Dépendances dev et optionnelles..."
pip install pytest pytest-cov pytest-mock ruff black mypy pre-commit bandit
pip install fastapi uvicorn pyinstaller

echo ""
echo "════════════════════════════════════════"
echo "  ✅ Installation terminée !"
echo "  Lance avec : ./run.sh"
echo "════════════════════════════════════════"
Rends-le exécutable et lance-le :

bash
chmod +x setup_all.sh
./setup_all.sh
💾 ESTIMATION DE LA TAILLE
Catégorie	Taille
Outils système (base)	~200 Mo
Cybersécurité (Metasploit, etc.)	~500 Mo
Environnement Python	~50 Mo
Dépendances base	~50 Mo
Dépendances dev	~200 Mo
Dépendances optionnelles	~100 Mo
TOTAL (sans IA)	~1.1 Go
Modèle IA (optionnel)	4-8 Go
TOTAL (avec IA)	~5-9 Go
🎯 PLAN DE PRIORITÉS
Priorité 1 — Minimum vital (1,1 Go)
Étape 1 (système)

Étape 2 (cyber)

Étape 3 (venv)

Étape 4 (Python base)

Priorité 2 — Qualité (200 Mo)
Étape 5 (dev)

Priorité 3 — Confort (100 Mo)
Étape 6 (optionnelles, sauf IA)

Priorité 4 — IA (5-9 Go)
Modèle Mistral 7B GGUF

🛠️ VÉRIFICATION APRÈS INSTALLATION
bash
cd ~/Bureau/Fokarat
source .venv/bin/activate

# Vérifier les outils
python3 --version
git --version
g++ --version
x86_64-w64-mingw32-g++ --version
msfvenom --version
ncat --version
apktool --version
upx --version
pytest --version
ruff --version
black --version
mypy --version

# Lancer FOKARAT
./run.sh
Dans le menu, choisis [17] (Vérifier les dépendances). Tout doit être en vert.

📞 Support
📧 Email : amissilwano5@gmail.com

🔗 GitHub : https://github.com/amissilwano5-beep/Fokarat/issues

FOKAS — Building the future, one tool at a time.



---

## 🎯 Commandes de création

```bash
cd ~/Bureau/Fokarat
source .venv/bin/activate

# Créer les dossiers
mkdir -p .github/ISSUE_TEMPLATE

# Sprint 4
nano core/mitre.py         # Colle le code MITRE
nano web/api.py            # Colle l'API stable
nano main.py               # Colle le main v3.3

# Sprint 5
nano CONTRIBUTING.md
nano ROADMAP.md
nano .github/ISSUE_TEMPLATE/bug_report.md
nano .github/ISSUE_TEMPLATE/feature_request.md
nano .github/PULL_REQUEST_TEMPLATE.md
nano INSTALLATION.md

# Tester
./run.sh
À tester dans le menu :

[33] : Générer un rapport MITRE (basé sur les actions déjà faites)

[34] : Export MITRE Navigator (JSON)

Dis-moi "Sprints 4 et 5 testés" une fois que les options [33] et [34] fonctionnent. Ensuite, on pourra :

Vérifier la structure GitHub finale

Faire un push propre

Créer une release v3.3 sur GitHub

Et n'oublie pas : efface tout et colle le nouveau contenu pour chaque fichier. C'est la règle. 💪

