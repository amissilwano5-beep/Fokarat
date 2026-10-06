 📖 FOKARAT - Documentation Complète/ pour t'aider à bien comprendre le framwork

Version 2.0 — Développé par Lwano Amissi Blanchard (FOKAS)


 🚀 Installation

```bash
git clone https://github.com/amissilwano5-beep/Fokarat.git
cd Fokarat
chmod +x install.sh run.sh
./install.sh

#Lancement

./run.sh

📋 Table des matières

1. Payload Python
2. Payload C++
3. Payload MSFVenom
4. Listener ncat
5. Listener Metasploit
6. Arrêter les listeners
7. Serveur HTTP
8. Générer DuckyScript
9. Encoder .duck → .bin
10. Flasher USB
11. APK Injector
12. Persistance WMI
13. Assistant IA
14. Configuration
15. Sauvegarder la config
16. Ouvrir msfconsole
17. Vérifier les dépendances
18. Crédits
19. Quitter



1. Payload Python

Menu : [01]

Génère un reverse shell Python avec reconnexion automatique.

Utilisation

1. Lance [01] dans le menu.
2. Saisis ton LHOST (ton IP d'écoute) — celle-ci est affichée par défaut si déjà configurée.
3. Saisis ton LPORT (le port d'écoute, entre 1 et 65535).
4. Le fichier payload_python.py est créé dans output/.
5. On te demande si tu veux compiler en .exe avec PyInstaller (o/n).
   · o : Compile en .exe (Windows), nécessite pyinstaller.
   · n : Garde juste le .py.

Utilisation du payload

Sur la cible :

```bash
python3 payload_python.py
```

Le shell se reconnecte automatiquement toutes les 5 secondes si la connexion tombe.

Commandes supportées

· Toute commande système
· cd <dir> pour changer de dossier
· exit ou quit pour terminer



2. Payload C++

Menu : [02]

Génère un reverse shell C++ compilé en .exe (Windows) ou binaire (Linux) via Mingw ou g++.

Utilisation

1. Lance [02].
2. Saisis LHOST et LPORT.
3. FOKARAT détecte automatiquement le compilateur :
   · x86_64-w64-mingw32-g++ → Windows 64-bit
   · i686-w64-mingw32-g++ → Windows 32-bit
   · g++ / clang++ → Linux
4. Le fichier payload_cpp.exe (ou payload_cpp) est créé dans output/.

Notes

· Compilation avec optimisation -O2.
· Payload autonome (pas besoin de Python sur la cible).



3. Payload MSFVenom

Menu : [03]

Génère un payload via msfvenom (comme TheFatRat).

Types de payload

Choix Payload Format
1 windows/x64/meterpreter/reverse_tcp .exe
2 windows/meterpreter/reverse_tcp .exe
3 linux/x64/meterpreter/reverse_tcp .elf
4 android/meterpreter/reverse_tcp .apk
5 osx/x64/meterpreter/reverse_tcp .macho
6 php/meterpreter/reverse_tcp .raw
7 python/meterpreter/reverse_tcp .raw
8 java/jsp_shell_reverse_tcp .raw

Utilisation

1. Lance [03].
2. Choisis le payload.
3. Saisis LHOST et LPORT.
4. Le fichier est créé dans output/fokarat_payload.<ext>.

Écoute

Utilise l'option [05] (Listener Metasploit) pour écouter.



4. Listener ncat

Menu : [04]

Lance un listener ncat (netcat moderne) sur un port.

Utilisation

1. Lance [04].
2. Saisis LHOST (généralement 0.0.0.0) et LPORT.
3. ncat écoute sur 0.0.0.0:<LPORT>.

Notes

· Idéal pour les reverse shells Python/C++.
· Requiert ncat (sudo apt install ncat).
· Arrêt automatique avec [06].



5. Listener Metasploit

Menu : [05]

Lance un handler Metasploit multi/handler.

Utilisation

1. Lance [05].
2. Choisis le payload à écouter :
   · [1] windows/x64/meterpreter/reverse_tcp
   · [2] windows/meterpreter/reverse_tcp
   · [3] linux/x64/meterpreter/reverse_tcp
   · [4] android/meterpreter/reverse_tcp
3. Saisis LHOST et LPORT.
4. Le fichier listener.rc est créé et Metasploit démarre en arrière-plan.

Notes

· ExitOnSession false : accepte plusieurs connexions.
· Utilise sessions -l dans msfconsole pour voir les sessions.



6. Arrêter les listeners

Menu : [06]

Arrête tous les listeners (ncat, Metasploit, HTTP server).

Utilisation

1. Lance [06].
2. Confirmation : tous les processus lancés par FOKARAT sont tués.



7. Serveur HTTP

Menu : [07]

Lance un serveur HTTP local pour :

· Servir les payloads (.ps1, .exe) au BadUSB.
· Recevoir les exfiltrations de fichiers.

Utilisation

1. Lance [07].
2. Saisis le port HTTP (défaut : 8080).
3. Le serveur sert le dossier output/.

Endpoints

· GET /* : sert les fichiers du dossier output/.
· POST /upload : reçoit les exfiltrations (BadUSB type 3).
  · Les fichiers sont sauvés dans output/exfil/.

Utilisation

Laisse tourner le serveur dans un terminal pendant que tu attaques avec le BadUSB.



8. Générer DuckyScript

Menu : [08]

Génère un script DuckyScript pour BadUSB.

Types d'attaque

Choix Description
1 Reverse Shell via Metasploit (payload.ps1)
2 Reverse Shell PowerShell direct
3 Vol de fichiers (exfiltration HTTP)
4 Ajout utilisateur admin caché
5 Téléchargement + exécution d'un .exe

Layouts clavier

Choix Layout
1 QWERTY (US)
2 AZERTY (France)
3 QWERTZ (Allemagne)
4 QWERTZ (Suisse)
5 QWERTY (UK)

Mode furtif (UAC Bypass)

· Non : Commande PowerShell directe (déclenche UAC).
· Oui : Contournement UAC via fodhelper.exe (invisible pour l'utilisateur).

Exemple de workflow (Reverse Shell MSF)

1. Lance [07] pour démarrer le serveur HTTP sur le port 8080.
2. Lance [08], choisis type 1, layout 1, mode furtif Oui.
3. Saisis LHOST et LPORT.
4. Fichiers générés :
   · output/inject.duck → à encoder
   · output/payload.ps1 → servi par le HTTP server
5. Lance [09] pour encoder.
6. Lance [10] pour flasher.



9. Encoder .duck → .bin

Menu : [09]

Compile un .duck en .bin compatible avec le matériel BadUSB.

Utilisation

1. Lance [09].
2. Saisis le chemin du fichier .duck (ex : output/inject.duck).
3. Le .bin est créé dans output/.

Méthodes utilisées

1. duckencoder.jar (Java) si trouvé dans tools/.
2. duckencoder.py (Python) si installé.
3. Sinon, téléchargement automatique de duckencoder.jar depuis GitHub.



10. Flasher USB

Menu : [10]

Flashe le .bin sur le matériel BadUSB.

Matériels supportés

Choix Matériel
1 Digispark (Attiny85)
2 Raspberry Pi Pico (pico-ducky)
3 USB Rubber Ducky (officiel)

Digispark

1. Nécessite micronucleus (sudo apt install micronucleus).
2. Convertit le .bin en .hex.
3. Débranche/rebranche le Digispark quand demandé.
4. Flash via micronucleus.

Raspberry Pi Pico

1. Branche le Pico en mode BOOTSEL (bouton maintenu).
2. Le Pico est monté comme volume RPI-RP2.
3. Le .bin est copié en .uf2.

USB Rubber Ducky

1. Insère la carte SD du Ducky.
2. Le fichier inject.bin est copié sur la carte.



11. APK Injector

Menu : [11]

Injecte un payload Metasploit dans un APK Android existant.

Utilisation

1. Lance [11].
2. Saisis le chemin de l'APK original.
3. Saisis LHOST et LPORT.
4. Choisis le payload :
   · [1] android/meterpreter/reverse_tcp
   · [2] android/meterpreter/reverse_https
   · [3] android/meterpreter/reverse_http

Étapes automatiques

1. Génération du payload APK via msfvenom.
2. Décompilation de l'APK original (apktool d).
3. Décompilation du payload.
4. Injection du code Smali dans l'APK original.
5. Hook dans le onCreate de la MainActivity.
6. Ajout des permissions manquantes dans le AndroidManifest.xml.
7. Recompilation (apktool b).
8. Alignement (zipalign).
9. Signature (jarsigner + keystore debug).

Résultat

Fichier output/fokarat_backdoored.apk.

Écoute

Utilise [05] avec le payload android/meterpreter/reverse_tcp.

Outils requis

apktool, msfvenom, jarsigner, keytool, zipalign.



12. Persistance WMI

Menu : [12]

Génère un script PowerShell de persistance WMI (Windows).

Utilisation

1. Lance [12].
2. Saisis le chemin du payload cible (sur Windows, ex : C:\payload.exe).
3. Le fichier output/wmi_persistence.ps1 est généré.

Sur la cible (Windows)

Exécute avec PowerShell administrateur :

```powershell
powershell -ExecutionPolicy Bypass -File wmi_persistence.ps1
```

Fonctionnement

· Crée un __EventFilter qui se déclenche toutes les heures.
· Crée un CommandLineEventConsumer qui lance le payload.
· Lie les deux avec __FilterToConsumerBinding.

Notes

· Persistance silencieuse (pas visible dans le démarrage).
· Requiert les droits administrateur pour installer.



13. Assistant IA

Menu : [13]

Chat avec une IA locale (optionnelle).

Utilisation

1. Lance [13].
2. Saisis ta question.
3. Réponse affichée.

Configuration

Nécessite :

· llama-cpp-python installé (pip install llama-cpp-python).
· Un modèle GGUF téléchargé dans models/ (ex : mistral-7b.gguf).
· Modifie config.yaml → llm_model_path.

Notes

· Aucune connexion Internet requise (IA 100% locale).
· Si aucun modèle n'est trouvé, un message d'erreur s'affiche.



14. Configuration

Menu : [14]

Modifie LHOST et LPORT par défaut.

Utilisation

1. Lance [14].
2. Saisis le nouveau LHOST (laisser vide pour garder l'actuel).
3. Saisis le nouveau LPORT (laisser vide pour garder l'actuel).

Notes

· Les modifications sont en mémoire uniquement.
· Lance [15] pour sauvegarder.



15. Sauvegarder la config

Menu : [15]

Sauvegarde la config actuelle dans config.yaml.

Utilisation

1. Lance [15].
2. Confirmation : config sauvegardée.

Contenu sauvegardé

· LHOST, LPORT, HTTP port, output dir, etc.



16. Ouvrir msfconsole

Menu : [16]

Lance Metasploit Framework en interactif.

Utilisation

1. Lance [16].
2. msfconsole s'ouvre.
3. Tape exit pour revenir à FOKARAT.



17. Vérifier les dépendances

Menu : [17]

Vérifie que tous les outils requis sont installés.

Outils vérifiés

· python3, pip, git
· g++, mingw-w64
· msfvenom, msfconsole
· ncat, apktool, jarsigner, zipalign, keytool, java
· pyinstaller

Résultat

· ✅ Vert : outil installé.
· ❌ Rouge : outil manquant + commande d'installation.



18. Crédits

Menu : [18]

Affiche les crédits et la licence.



19. Quitter

Menu : [19]

Quitte FOKARAT en arrêtant tous les listeners.



⚠️ Avertissement légal

FOKARAT est un outil éducatif et de recherche en sécurité. 
L'utiliser sur des systèmes sans autorisation écrite est illégal. 
L'auteur décline toute responsabilité en cas d'usage abusif.



📞 Support

· Auteur : Lwano Amissi Blanchard (FOKAS)
· GitHub : github.com/amissilwano5-beep
· Email : amissilwano5@gmail.com
· Localisation : Bukavu, RDC
