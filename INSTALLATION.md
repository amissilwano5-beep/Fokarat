
# 📦 FOKARAT - Guide d'Installation Complet

**Version 4.0 — Octobre 2026**

Ce document liste **TOUT** ce qu'il faut installer pour que FOKARAT fonctionne à 100%.

---

## 🎯 État actuel

**FOKARAT fonctionne à ~60%** sans rien installer (options éducatives, générateurs, plugins, rapports).

Pour les modules avancés (post-exploitation, C2, mobile), il faut installer les outils ci-dessous.

---

## 🔧 ÉTAPE 1 : Outils système (APT)

```bash
sudo apt update
sudo apt install -y \
    python3 python3-pip python3-venv \
    git make build-essential \
    g++ gcc

🔧 ÉTAPE 2 : Outils cybersécurité (APT)
sudo apt install -y \
    mingw-w64 \
    ncat \
    metasploit-framework \
    apktool \
    default-jdk \
    zipalign \
    upx-ucl \
    binutils-avr

🔧 ÉTAPE 3 : Environnement Python
bash
cd ~/Bureau/Fokarat
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

🔧 ÉTAPE 4 : Dépendances Python (base)
bash
pip install -r requirements.txt

 ÉTAPE 5 : Sprint 7 - Post-exploitation Windows
bash
pip install impacket evil-winrm pypykatz

ÉTAPE 6 : Sprint 8 - Post-exploitation Linux
bash
sudo apt install -y sshpass ansible docker.io socat
pip install kubectl

 ÉTAPE 7 : Sprint 9 - C2 et Pivoting
bash
sudo apt install -y proxychains4 ssh
# Chisel : 
# Télécharger depuis https://github.com/jpillora/chisel/releases
# Ligolo-ng : 
# Télécharger depuis https://github.com/nicocha30/ligolo-ng/releases

🔧 ÉTAPE 8 : Sprint 10 - Post-exploitation Mobile
bash
sudo apt install -y adb libimobiledevice-utils
pip install frida frida-tools objection

🔧 ÉTAPE 9 : Sprint 11 - Rapports PDF
bash
pip install reportlab

🔧 ÉTAPE 10 : Outils de développement (optionnel)
bash
pip install -r requirements-dev.txt
🚀 INSTALLATION AUTOMATIQUE (tout-en-un):

#!/bin/bash
set -e

echo "════════════════════════════════════════"
echo "  FOKARAT v4.0 - Installation complète"
echo "════════════════════════════════════════"

echo ""
echo "[1/9] Outils système..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git make build-essential g++ gcc

echo ""
echo "[2/9] Outils cybersécurité..."
sudo apt install -y mingw-w64 ncat metasploit-framework apktool default-jdk \
    zipalign upx-ucl binutils-avr

echo ""
echo "[3/9] Environnement virtuel..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

echo ""
echo "[4/9] Dépendances Python base..."
pip install -r requirements.txt

echo ""
echo "[5/9] Sprint 7 - Windows..."
pip install impacket evil-winrm pypykatz

echo ""
echo "[6/9] Sprint 8 - Linux..."
sudo apt install -y sshpass ansible docker.io socat

echo ""
echo "[7/9] Sprint 9 - C2 + Pivoting..."
sudo apt install -y proxychains4 ssh

echo ""
echo "[8/9] Sprint 10 - Mobile..."
sudo apt install -y adb libimobiledevice-utils
pip install frida frida-tools objection

echo ""
echo "[9/9] Sprint 11 - Rapports..."
pip install reportlab

echo ""
echo "════════════════════════════════════════"
echo "  ✅ Installation terminée !"
echo "  Lance : ./run.sh"
echo "════════════════════════════════════════"

Rends exécutable et lance :

bash
chmod +x setup_all.sh
./setup_all.sh

💾 ESTIMATION TOTALE
Catégorie	Taille
Outils système	~250 Mo
Cybersécurité (Metasploit, etc.)	~500 Mo
Python base	~80 Mo
Sprint 7 (Windows)	~30 Mo
Sprint 8 (Linux)	~500 Mo
Sprint 9 (C2)	~20 Mo
Sprint 10 (Mobile)	~100 Mo
Sprint 11 (PDF)	~5 Mo
TOTAL MINIMUM	~1.5 Go
Avec dev tools	~1.75 Go

🎯 VÉRIFICATION
bash
cd ~/Bureau/Fokarat
source .venv/bin/activate
./run.sh
Puis dans le menu : [17] — Vérifier les dépendances.

Tout doit être en vert (sauf les options non installées).

📞 Support
📧 amissilwano5@gmail.com

🐙 github.com/amissilwano5-beep/Fokarat/issues

FOKAS — Building the future, one tool at a time.

