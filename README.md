# FOKARAT

Framework de cybersécurité développé par FOKAS.

> ⚠️ **Usage éducatif uniquement.** Ne jamais utiliser sur des systèmes sans autorisation écrite.

## Installation

```bash
git clone <votre-repo>
cd Fokarat
chmod +x install.sh && ./install.sh

#Utilisation

./run.sh

Le menu vous guide pour :

Générer des payloads (Python, C++, MSFVenom)

Lancer des listeners (ncat, Metasploit)

Créer des scripts BadUSB

Injecter des payloads dans des APK

Installer une persistance WMI

Auteur
Lwano Amissi Blanchard (FOKAS) — Bukavu, RDC

##final

```bash
chmod +x run.sh install.sh
./run.sh


# 1. Dépendances système
sudo apt update
sudo apt install -y python3-pip python3-venv git g++ mingw-w64 ncat \
    apktool default-jdk zipalign binutils-avr

# 2. Environnement virtuel
cd ~/Bureau/FOKARAT
python3 -m venv .venv
source .venv/bin/activate

# 3. Dépendances Python
pip install -r requirements.txt

# 4. Lancer
chmod +x run.sh main.py
./run.sh