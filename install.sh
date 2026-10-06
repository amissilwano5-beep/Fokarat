#!/bin/bash
# FOKARAT - Script d'installation

set -e

echo "======================================"
echo "  Installation de FOKARAT"
echo "======================================"

# Détection de l'OS
if [ -f /etc/debian_version ]; then
    echo "[+] Debian/Ubuntu/Kali détecté."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv git g++ mingw-w64 ncat \
        apktool default-jdk metasploit-framework upx-ucl
else
    echo "[!] OS non Debian. Installez manuellement : python3, pip, g++, mingw, ncat, apktool, metasploit."
fi

echo "[+] Création de l'environnement virtuel..."
python3 -m venv .venv
source .venv/bin/activate

echo "[+] Installation des dépendances Python..."
pip install --upgrade pip
pip install -r requirements.txt

chmod +x main.py run.sh

echo ""
echo "======================================"
echo "  Installation terminée !"
echo "  Lancez avec : ./run.sh"
echo "======================================"