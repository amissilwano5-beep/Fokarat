

📄 DOCUMENTATION.md (Version 2.0)

```markdown
# 📖 FOKARAT - Documentation Complète

**Version 3.0** — Développé par Lwano Amissi Blanchard (FOKAS)

---

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/amissilwano5-beep/Fokarat.git
cd Fokarat
```

2. Installation automatique

```bash
chmod +x install.sh run.sh
./install.sh
```

3. Lancer FOKARAT

```bash
./run.sh
```

Prérequis

· OS : Kali Linux, Ubuntu 22.04+, Debian 11+
· Python : 3.8+
· Espace disque : 2 Go minimum
· RAM : 2 Go minimum

Les dépendances système sont installées automatiquement par install.sh.

---

📋 Table des matières

🎯 Payloads

1. Payload Python
2. Payload C++
3. Payload MSFVenom

🎧 Listeners

4. Listener ncat
5. Listener Metasploit
6. Arrêter les listeners
7. Serveur HTTP

💾 BadUSB

8. Générer DuckyScript
9. Encoder .duck → .bin
10. Flasher USB

⚔️ Attaques

11. APK Injector
12. Persistance WMI

🛡️ Évasion Antivirus

20. Padding aléatoire C++
21. Obfuscation Python
22. Compression UPX
23. Multi-encodage MSFVenom
24. Protection Anti-VM
25. Protection Anti-Debug

🛠️ Divers

13. Assistant IA
14. Configuration
15. Sauvegarder la config
16. Ouvrir msfconsole
17. Vérifier les dépendances
18. Rapport d'opérations
19. API Web
20. Crédits
21. Quitter

---

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

💡 Astuce

Combine avec [21] (obfuscation Python) pour rendre le payload indétectable.

---

2. Payload C++

Menu : [02]

Génère un reverse shell C++ compilé en .exe (Windows) ou binaire (Linux).

Utilisation

1. Lance [02].
2. Saisis LHOST et LPORT.
3. FOKARAT détecte automatiquement le compilateur :
   · x86_64-w64-mingw32-g++ → Windows 64-bit
   · i686-w64-mingw32-g++ → Windows 32-bit
   · g++ / clang++ → Linux
4. Le fichier payload_cpp.exe (ou payload_cpp) est créé dans output/.

💡 Astuce

Combine avec [20] (padding) et [22] (UPX) pour un payload FUD (Fully Undetectable).

---

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

---

4. Listener ncat

Menu : [04]

Lance un listener ncat (netcat moderne).

Utilisation

1. Lance [04].
2. Saisis LHOST (généralement 0.0.0.0) et LPORT.
3. ncat écoute sur 0.0.0.0:<LPORT>.

Notes

· Idéal pour les reverse shells Python/C++.
· Requiert ncat (sudo apt install ncat).
· Arrêt automatique avec [06].

---

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

---

6. Arrêter les listeners

Menu : [06]

Arrête tous les listeners (ncat, Metasploit, HTTP server).

---

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
· POST /upload : reçoit les exfiltrations.
  · Les fichiers sont sauvés dans output/exfil/.

---

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
· Oui : Contournement UAC via fodhelper.exe (invisible).

Workflow complet

1. Lance [07] pour démarrer le serveur HTTP sur le port 8080.
2. Lance [08], choisis type 1, layout 1, mode furtif Oui.
3. Saisis LHOST et LPORT.
4. Fichiers générés :
   · output/inject.duck → à encoder
   · output/payload.ps1 → servi par le HTTP server
5. Lance [09] pour encoder.
6. Lance [10] pour flasher.

---

9. Encoder .duck → .bin

Menu : [09]

Compile un .duck en .bin compatible avec le matériel BadUSB.

Utilisation

1. Lance [09].
2. Saisis le chemin du fichier .duck.
3. Le .bin est créé dans output/.

Méthodes

1. duckencoder.jar (Java) si trouvé dans tools/.
2. duckencoder.py (Python) si installé.
3. Sinon, téléchargement automatique depuis GitHub.

---

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

Raspberry Pi Pico

1. Branche le Pico en mode BOOTSEL.
2. Monté comme volume RPI-RP2.
3. Le .bin est copié en .uf2.

USB Rubber Ducky

1. Insère la carte SD du Ducky.
2. inject.bin est copié sur la carte.

---

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
4. Injection du code Smali.
5. Hook dans le onCreate de la MainActivity.
6. Ajout des permissions manquantes.
7. Recompilation (apktool b).
8. Alignement (zipalign).
9. Signature (jarsigner).

Résultat

Fichier output/fokarat_backdoored.apk.

Outils requis

apktool, msfvenom, jarsigner, keytool, zipalign.

---

12. Persistance WMI

Menu : [12]

Génère un script PowerShell de persistance WMI (Windows).

Utilisation

1. Lance [12].
2. Saisis le chemin du payload cible (ex : C:\payload.exe).
3. Le fichier output/wmi_persistence.ps1 est généré.

Sur la cible (Windows)

```powershell
powershell -ExecutionPolicy Bypass -File wmi_persistence.ps1
```

Fonctionnement

· Crée un __EventFilter qui se déclenche toutes les heures.
· Crée un CommandLineEventConsumer qui lance le payload.
· Lie les deux avec __FilterToConsumerBinding.

Notes

· Persistance silencieuse (invisible dans le démarrage).
· Requiert les droits administrateur.

---

20. Padding aléatoire C++

Menu : [20]

Rend un payload C++ FUD (Fully Undetectable) en ajoutant du code mort aléatoire.

Utilisation

1. Lance [20].
2. Saisis le chemin du fichier .c à protéger.
3. FOKARAT génère un fichier <nom>_protected.c.

Ce qui est ajouté

· 16 Ko de padding binaire aléatoire (avant + après le payload).
· 15 fonctions factices qui ne font rien.
· Appels au démarrage pour tromper l'analyse statique.
· Signature unique à chaque compilation (pas de hash identique).

Résultat

Un payload qui change d'apparence à chaque compilation, rendant la détection par signature impossible.

💡 Astuce

Après [20], compile le .c protégé avec Mingw, puis applique [22] (UPX).

---

21. Obfuscation Python

Menu : [21]

Rend un payload Python indétectable par obfuscation multi-couches.

Utilisation

1. Lance [21].
2. Saisis le chemin du fichier .py.
3. FOKARAT génère <nom>_obf.py.

Couches d'obfuscation

1. XOR avec clé aléatoire de 32 octets.
2. Compression zlib niveau maximum.
3. Base64 du résultat.
4. Découpage en morceaux de 80 caractères.
5. Exécution dynamique via compile() + exec().

Résultat

Le code source original n'apparaît nulle part. Même en ouvrant le fichier, tu ne vois que du Base64.

---

22. Compression UPX

Menu : [22]

Compresse un binaire avec UPX ultra-brute.

Utilisation

1. Lance [22].
2. Saisis le chemin du binaire (.exe, .elf).
3. FOKARAT compresse et remplace l'original.

Résultat

· Taille réduite de 50-70%.
· Signature binaire modifiée (évasion antivirus).

Notes

· Requiert upx-ucl (sudo apt install upx-ucl).
· Mode --ultra-brute = compression maximale.
· Ne fonctionne pas sur les binaires signés.

---

23. Multi-encodage MSFVenom

Menu : [23]

Encode un payload MSFVenom plusieurs fois avec des encodeurs polymorphes.

Encodeurs disponibles

Choix Encodeur Description
1 x86/shikata_ga_nai Polymorphe x86 (recommandé)
2 x64/xor_dynamic XOR dynamique x64
3 x86/countdown Compteur décroissant
4 x86/fnstenv_mov FNSTENV+MOV
5 x86/jmp_call_additive JMP/CALL additif
6 x86/alpha_mixed Alpha alphanumérique
7 cmd/powershell_base64 PowerShell Base64

Utilisation

1. Lance [23].
2. Choisis l'encodeur.
3. Saisis LHOST et LPORT.
4. Saisis le nombre d'itérations (défaut : 5).
5. Le payload est généré dans output/payload_encoded_<n>.exe.

Résultat

Chaque itération multiplie les chances d'évasion antivirus.

---

24. Protection Anti-VM

Menu : [24]

Ajoute une détection de VM/sandbox à un payload C++.

Utilisation

1. Lance [24].
2. Saisis le chemin du .c à protéger.
3. FOKARAT génère <nom>_antivm.c.

Détections ajoutées

1. Fenêtres VMware/VirtualBox/QEMU
2. Fichiers drivers (vmmouse.sys, VBoxMouse.sys, etc.)
3. RAM < 2 Go (probable sandbox)
4. CPU < 2 cœurs
5. Nom de machine (SANDBOX, MALWARE, VIRUS, CUCKOO...)
6. Nom d'utilisateur (sandbox, malware, virus...)

Comportement

Si une VM est détectée, le payload s'arrête immédiatement (return 1).

---

25. Protection Anti-Debug

Menu : [25]

Ajoute une détection de debugger à un payload C++.

Utilisation

1. Lance [25].
2. Saisis le chemin du .c à protéger.
3. FOKARAT génère <nom>_antidbg.c.

Détections ajoutées

1. IsDebuggerPresent() (API Windows)
2. CheckRemoteDebuggerPresent()
3. PEB->BeingDebugged (lecture directe du processus)
4. Timing attack (les debuggers ralentissent)
5. Hardware breakpoints (Dr0-Dr3)

Comportement

Si un debugger est détecté, le payload s'arrête immédiatement.

---

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
· Un modèle GGUF dans models/ (ex : mistral-7b.gguf).
· Modifie config.yaml → llm_model_path.

Notes

· Aucune connexion Internet requise (IA 100% locale).
· Si aucun modèle n'est trouvé, un message d'erreur s'affiche.

---

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

---

15. Sauvegarder la config

Menu : [15]

Sauvegarde la config actuelle dans config.yaml.

Contenu sauvegardé

LHOST, LPORT, HTTP port, output dir, etc.

---

16. Ouvrir msfconsole

Menu : [16]

Lance Metasploit Framework en interactif.

Utilisation

1. Lance [16].
2. msfconsole s'ouvre.
3. Tape exit pour revenir à FOKARAT.

---

17. Vérifier les dépendances

Menu : [17]

Vérifie que tous les outils requis sont installés.

Outils vérifiés

· python3, pip, git
· g++, mingw-w64
· msfvenom, msfconsole
· ncat, apktool, jarsigner, zipalign, keytool, java
· upx (nouveau)
· pyinstaller

Résultat

· ✅ Vert : outil installé.
· ❌ Rouge : outil manquant + commande d'installation.

---

26. Rapport d'opérations

Menu : [26]

Génère un rapport Markdown de toutes tes opérations.

Utilisation

1. Lance [26].
2. Le rapport est généré dans output/fokarat_report.md et affiché à l'écran.

Contenu du rapport

· Liste de tous les payloads générés (date, type, LHOST, LPORT, taille, statut).
· Liste de tous les listeners lancés.
· Statistiques globales.

Base de données

Toutes les opérations sont automatiquement enregistrées dans output/fokarat.db (SQLite).

Structure de la base

· Table payloads : tous les payloads générés.
· Table listeners : tous les listeners lancés.
· Table sessions : sessions (extensible).

---

27. API Web

Menu : [27]

Lance une API REST (FastAPI) pour piloter FOKARAT depuis un navigateur.

Utilisation

1. Lance [27].
2. Ouvre ton navigateur : http://localhost:5000/docs

Endpoints

Méthode URL Description
GET / Statut du framework
GET /health Healthcheck
POST /payload/python Générer un payload Python
GET /payloads Liste tous les payloads
GET /report Générer un rapport

Prérequis

```bash
pip install fastapi uvicorn
```

Exemple d'appel

```bash
curl -X POST http://localhost:5000/payload/python \
  -H "Content-Type: application/json" \
  -d '{"type":"python","lhost":"192.168.1.100","lport":4444}'
```

Notes

· L'API tourne sur le port 5000 par défaut.
· Interface Swagger UI intégrée sur /docs.
· Aucune authentification (à utiliser en local uniquement).


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

 Workflows Recommandés

Workflow 1 : Payload Windows FUD complet

1. [02] Générer le payload C++.
2. [20] Appliquer le padding aléatoire.
3. Compiler le .c protégé avec Mingw.
4. [22] Compresser avec UPX.
5. [05] Lancer le listener Metasploit.
6. Envoyer le payload sur la cible.

Workflow 2 : BadUSB Complet

1. [07] Démarrer le serveur HTTP.
2. [08] Générer le DuckyScript (Reverse Shell MSF).
3. [09] Encoder le .duck en .bin.
4. [10] Flasher sur Digispark/Pico.
5. Brancher sur la cible.
6. [05] Listener Metasploit pour recevoir le shell.

Workflow 3 : APK Android compromis

1. [11] Injecter un payload dans un APK.
2. [05] Lancer le listener Metasploit (Android).
3. Envoyer l'APK à la cible.
4. Attendre la connexion.

Workflow 4 : Audit complet

1. Générer plusieurs payloads ([01], [02], [03]).
2. [20] à [25] appliquer toutes les protections.
3. [26] Générer le rapport final.
4. [27] Consulter l'API pour automatiser.



📞 Support

· Auteur : Lwano Amissi Blanchard (FOKAS)
· GitHub : github.com/amissilwano5-beep
· Email : amissilwano5@gmail.com
· Localisation : Bukavu, RDC

