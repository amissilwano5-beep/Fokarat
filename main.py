#!/usr/bin/env python3
"""FOKARAT v2.0 - Interface animée"""
import os
import sys
import time
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import Config
from core.logger import Logger
from core.utils import which
from modules.payload_generators.python_gen import PythonPayloadGenerator
from modules.payload_generators.cpp_gen import CppPayloadGenerator
from modules.payload_generators.msfvenom_gen import MsfvenomGenerator
from modules.listeners.listener_manager import ListenerManager
from modules.injectors.badusb_gen import BadUSBGenerator
from modules.injectors.duck_encoder import DuckEncoder
from modules.injectors.usb_flasher import USBFlasher
from modules.injectors.http_server import HTTPServer
from modules.android.apk_injector import ApkInjector
from modules.persistence.wmi_persist import WMIPersistence
from ai.assistant import Assistant

logger = Logger()
config = Config()
listener = ListenerManager()
http_server = HTTPServer()


# ══════════════════════════════════════════════════
#  COULEURS ANSI
# ══════════════════════════════════════════════════
class C:
    R = "\033[0m"       # Reset
    B = "\033[1m"       # Bold
    D = "\033[2m"       # Dim
    RED = "\033[91m"
    GRN = "\033[92m"
    YEL = "\033[93m"
    BLU = "\033[94m"
    MAG = "\033[95m"
    CYN = "\033[96m"
    WHT = "\033[97m"
    OR = "\033[38;5;208m"


# ══════════════════════════════════════════════════
#  BANNIÈRE ASCII
# ══════════════════════════════════════════════════
BANNER = f"""{C.GRN}{C.B}
   ███████╗ ██████╗ ██╗  ██╗ █████╗ ██████╗  █████╗ ████████╗
   ██╔════╝██╔═══██╗██║ ██╔╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
   █████╗  ██║   ██║█████╔╝ ███████║██████╔╝███████║   ██║   
   ██╔══╝  ██║   ██║██╔═██╗ ██╔══██║██╔══██╗██╔══██║   ██║   
   ██║     ╚██████╔╝██║  ██╗██║  ██║██║  ██║██║  ██║   ██║   
   ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   {C.R}
{C.CYN}{C.B}              Building the future, one tool at a time.{C.R}
{C.YEL}                       FOKARAT Framework v2.0{C.R}
"""

BOOT_SEQUENCE = [
    ("[BOOT 01] Initialisation du noyau FOKARAT...", 0.15),
    ("[BOOT 02] Chargement des modules payloads...", 0.15),
    ("[BOOT 03] Chargement des listeners...", 0.15),
    ("[BOOT 04] Chargement des modules Android...", 0.15),
    ("[BOOT 05] Chargement de l'assistant IA...", 0.15),
    ("[BOOT 06] Vérification des dépendances...", 0.20),
    ("[BOOT 07] Système prêt pour la session.", 0.30),
]


# ══════════════════════════════════════════════════
#  FONCTIONS D'ANIMATION
# ══════════════════════════════════════════════════
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def typewriter(text, delay=0.008, color=C.WHT):
    """Effet machine à écrire."""
    for char in text:
        sys.stdout.write(f"{color}{char}{C.R}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def spinner(duration=0.6, message="Chargement", color=C.CYN):
    """Affiche un spinner animé."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r  {color}{frames[i % len(frames)]}{C.R} {message}...")
        sys.stdout.flush()
        time.sleep(0.06)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")


def progress_bar(duration=0.8, width=40, color=C.GRN):
    """Barre de progression animée."""
    sys.stdout.write("  ")
    for i in range(width + 1):
        pct = int(i / width * 100)
        filled = "█" * i
        empty = "░" * (width - i)
        sys.stdout.write(f"\r  {color}{filled}{C.D}{empty}{C.R} {C.B}{pct:3d}%{C.R}")
        sys.stdout.flush()
        time.sleep(duration / width)
    print()


def boot_animation():
    """Animation de démarrage complète."""
    clear()
    for msg, delay in BOOT_SEQUENCE:
        typewriter(f"  {C.YEL}{msg}{C.R}", delay=0.004)
        time.sleep(delay)
    print()
    progress_bar(0.6, 50, C.CYN)
    time.sleep(0.2)


def animated_banner():
    """Bannière avec effet d'apparition."""
    clear()
    print()
    for line in BANNER.split("\n"):
        print(f"  {line}")
        time.sleep(0.03)
    print()


# ══════════════════════════════════════════════════
#  MENU PRINCIPAL STYLÉ
# ══════════════════════════════════════════════════
def separator(char="═", length=62, color=C.CYN):
    return f"{color}{char * length}{C.R}"


def menu_option(key, label, color=C.WHT):
    return f"  {C.YEL}│{C.R}  {C.GRN}[{key}]{C.R}  {color}{label}{C.R}"


def show_menu():
    clear()
    animated_banner()

    lhost = config.get("lhost") or f"{C.RED}(non défini){C.R}"
    lport = config.get("lport")
    out = config.get("output_dir", "output")

    print(f"  {C.MAG}◆{C.R} LHOST : {C.CYN}{lhost}{C.R}       "
          f"{C.MAG}◆{C.R} LPORT : {C.CYN}{lport}{C.R}       "
          f"{C.MAG}◆{C.R} Output : {C.CYN}{out}{C.R}")
    print()

    print(separator("═", 62, C.CYN))

    # Section Payloads
    print(f"  {C.B}{C.MAG}▶ PAYLOADS{C.R}")
    print(menu_option("01", "Payload Python (reverse shell)"))
    print(menu_option("02", "Payload C++ (Mingw)"))
    print(menu_option("03", "Payload MSFVenom"))

    print(separator("─", 62, C.BLU))

    # Section Listeners
    print(f"  {C.B}{C.MAG}▶ LISTENERS{C.R}")
    print(menu_option("04", "Listener ncat"))
    print(menu_option("05", "Listener Metasploit"))
    print(menu_option("06", "Arrêter tous les listeners", C.RED))
    print(menu_option("07", "Serveur HTTP (payloads / exfil)"))

    print(separator("─", 62, C.BLU))

    # Section BadUSB
    print(f"  {C.B}{C.MAG}▶ BADUSB{C.R}")
    print(menu_option("08", "Générer DuckyScript (5 types d'attaques)"))
    print(menu_option("09", "Encoder .duck → .bin"))
    print(menu_option("10", "Flasher sur matériel USB (Digispark / Pico / Ducky)"))

    print(separator("─", 62, C.BLU))

    # Section Attaques
    print(f"  {C.B}{C.MAG}▶ ATTAQUES{C.R}")
    print(menu_option("11", "APK Injector (Android)"))
    print(menu_option("12", "Persistance WMI (Windows)"))

    print(separator("─", 62, C.BLU))

    # Section Divers
    print(f"  {C.B}{C.MAG}▶ DIVERS{C.R}")
    print(menu_option("13", "Assistant IA local"))
    print(menu_option("14", "Configuration LHOST / LPORT"))
    print(menu_option("15", "Sauvegarder la config"))
    print(menu_option("16", "Ouvrir msfconsole"))
    print(menu_option("17", "Vérifier les dépendances"))
    print(menu_option("18", "Crédits"))
    print(menu_option("19", "Quitter", C.RED))

    print(separator("═", 62, C.CYN))
    print()


# ══════════════════════════════════════════════════
#  VÉRIFICATION DES DÉPENDANCES
# ══════════════════════════════════════════════════
def check_dependencies():
    clear()
    animated_banner()
    print(f"  {C.B}{C.CYN}═══ VÉRIFICATION DES DÉPENDANCES ═══{C.R}\n")

    deps = {
        "python3": "Interpréteur Python",
        "pip": "Gestionnaire Python",
        "git": "Contrôle de version",
        "g++": "Compilateur C++",
        "x86_64-w64-mingw32-g++": "Compilateur Mingw64",
        "msfvenom": "Générateur Metasploit",
        "msfconsole": "Console Metasploit",
        "ncat": "Netcat moderne",
        "apktool": "Décompilation APK",
        "jarsigner": "Signature Java",
        "zipalign": "Alignement APK",
        "keytool": "Gestion keystore",
        "java": "Java Runtime",
        "pyinstaller": "Compil Python → exe",
    }

    missing = []
    for cmd, desc in deps.items():
        spinner(0.15, f"Vérification de {cmd}")
        if which(cmd):
            print(f"  {C.GRN}[✓]{C.R} {C.B}{cmd:<28}{C.R} {C.D}{desc}{C.R}")
        else:
            print(f"  {C.RED}[✗]{C.R} {C.B}{cmd:<28}{C.R} {C.D}{desc}{C.R}")
            missing.append(cmd)

    print()
    if missing:
        logger.warning(f"{len(missing)} outil(s) manquant(s).")
        print(f"\n  {C.YEL}Installation :{C.R}")
        print(f"    {C.CYN}sudo apt install python3 python3-pip git g++ mingw-w64 ncat apktool default-jdk zipalign binutils-avr{C.R}")
        print(f"    {C.CYN}pip install pyinstaller llama-cpp-python{C.R}")
    else:
        logger.success("Toutes les dépendances sont présentes !")
    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")


# ══════════════════════════════════════════════════
#  MENU PRINCIPAL
# ══════════════════════════════════════════════════
def main():
    boot_animation()
    time.sleep(0.3)

    while True:
        show_menu()
        choice = input(f"  {C.B}{C.MAG}╰─▶{C.R} {C.B}FOKARAT{C.R} {C.YEL}>{C.R} ").strip()

        try:
            # PAYLOADS
            if choice == "01":
                spinner(0.4, "Préparation du module Python")
                PythonPayloadGenerator().run(config)
            elif choice == "02":
                spinner(0.4, "Préparation du module C++")
                CppPayloadGenerator().run(config)
            elif choice == "03":
                spinner(0.4, "Préparation de MSFVenom")
                MsfvenomGenerator().run(config)

            # LISTENERS
            elif choice == "04":
                spinner(0.3, "Démarrage ncat")
                listener.start_ncat(config)
            elif choice == "05":
                spinner(0.3, "Démarrage Metasploit")
                listener.start_msf(config)
            elif choice == "06":
                listener.stop_all()
            elif choice == "07":
                http_server.run(config)
                continue

            # BADUSB
            elif choice == "08":
                spinner(0.3, "Préparation DuckyScript")
                BadUSBGenerator().run(config)
            elif choice == "09":
                DuckEncoder().run(config)
            elif choice == "10":
                USBFlasher().run(config)

            # ATTAQUES
            elif choice == "11":
                spinner(0.4, "Préparation APK Injector")
                ApkInjector().run(config)
            elif choice == "12":
                WMIPersistence().run(config)

            # DIVERS
            elif choice == "13":
                q = input(f"  {C.CYN}Question >{C.R} ").strip()
                print()
                spinner(0.5, "Réflexion de l'IA")
                print(Assistant(config.get("llm_model_path")).chat(q))
            elif choice == "14":
                print()
                new_ip = input(f"  {C.YEL}Nouveau LHOST [{config.get('lhost')}]{C.R} : ").strip()
                if new_ip:
                    config.set("lhost", new_ip)
                new_port = input(f"  {C.YEL}Nouveau LPORT [{config.get('lport')}]{C.R} : ").strip()
                if new_port.isdigit():
                    config.set("lport", int(new_port))
                spinner(0.3, "Mise à jour")
                logger.success("Configuration mise à jour.")
            elif choice == "15":
                spinner(0.3, "Sauvegarde")
                if config.save():
                    logger.success("Config sauvegardée dans config.yaml")
            elif choice == "16":
                if which("msfconsole"):
                    spinner(0.4, "Ouverture de msfconsole")
                    os.system("msfconsole")
                else:
                    logger.error("msfconsole absent.")
            elif choice == "17":
                check_dependencies()
                continue
            elif choice == "18":
                clear()
                animated_banner()
                print(f"  {C.B}{C.GRN}FOKARAT v2.0{C.R}")
                print(f"  {C.WHT}Auteur  :{C.R} Lwano Amissi Blanchard (FOKAS)")
                print(f"  {C.WHT}Email   :{C.R} amissilwano5@gmail.com")
                print(f"  {C.WHT}GitHub  :{C.R} github.com/amissilwano5-beep")
                print(f"  {C.WHT}Ville   :{C.R} Bukavu, RDC")
                print()
                print(f"  {C.YEL}⚠  Usage éducatif et tests autorisés uniquement.{C.R}")
            elif choice == "19":
                print()
                spinner(0.5, "Arrêt des services")
                listener.stop_all()
                typewriter(f"\n  {C.GRN}Merci d'avoir utilisé FOKARAT. À bientôt !{C.R}", delay=0.02)
                print()
                break
            else:
                logger.warning("Choix invalide.")

        except KeyboardInterrupt:
            print()
            logger.warning("Action interrompue.")
        except Exception as e:
            logger.error(f"Erreur : {e}")

        input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        listener.stop_all()
        print(f"\n{C.RED}[!] Sortie forcée.{C.R}")