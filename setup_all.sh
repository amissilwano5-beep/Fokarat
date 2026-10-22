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
chmod +x setup_all.sh
./setup_all.sh

🎯 VÉRIFICATION
bash
cd ~/Bureau/Fokarat
source .venv/bin/activate
./run.sh
