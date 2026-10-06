"""
FOKARAT - Flasheur USB BadUSB
Détecte et flashe automatiquement un Digispark ou Raspberry Pi Pico.
"""
import os
import subprocess
import time
from core.module_interface import ModuleInterface
from core.logger import Logger
from core.utils import which, safe_input

logger = Logger()


class USBFlasher(ModuleInterface):
    def get_metadata(self):
        return {
            "name": "USB Flasher",
            "version": "1.0",
            "type": "flasher",
            "description": "Flashe un .bin sur Digispark ou Raspberry Pi Pico."
        }

    def run(self, config):
        print("\n  Matériel cible :")
        print("    [1] Digispark (Attiny85)")
        print("    [2] Raspberry Pi Pico (pico-ducky)")
        print("    [3] USB Rubber Ducky (officiel)")
        choice = safe_input("  [>] Choix [1] : ") or "1"

        bin_file = safe_input("  [>] Chemin du fichier .bin : ").strip()
        if not os.path.exists(bin_file):
            logger.error("Fichier .bin introuvable.")
            return {"status": "error", "message": "Fichier introuvable"}

        if choice == "1":
            return self._flash_digispark(bin_file)
        elif choice == "2":
            return self._flash_pico(bin_file)
        elif choice == "3":
            return self._flash_rubber_ducky(bin_file)
        return {"status": "error", "message": "Choix invalide"}

    def _flash_digispark(self, bin_file):
        """Digispark : conversion .bin -> .hex puis upload via micronucleus."""
        if not which("micronucleus"):
            logger.error("micronucleus non installé. sudo apt install micronucleus")
            return {"status": "error", "message": "micronucleus manquant"}

        hex_file = bin_file.replace(".bin", ".hex")
        if not which("avr-objcopy"):
            logger.error("avr-objcopy manquant. sudo apt install binutils-avr")
            return {"status": "error", "message": "avr-objcopy manquant"}

        logger.info("Conversion .bin -> .hex...")
        try:
            with open(bin_file, "rb") as f:
                data = f.read()
            # Encodage Intel HEX
            lines = []
            for i in range(0, len(data), 16):
                chunk = data[i:i + 16]
                addr = i & 0xFFFF
                rec = f":{len(chunk):02X}{addr:04X}00" + "".join(f"{b:02X}" for b in chunk)
                checksum = (-sum(int(rec[j:j + 2], 16) for j in range(1, len(rec), 2))) & 0xFF
                lines.append(rec + f"{checksum:02X}")
            lines.append(":00000001FF")
            with open(hex_file, "w") as f:
                f.write("\n".join(lines))

            logger.info("Flashage sur Digispark (débranchez/rebranchez)...")
            subprocess.run(["micronucleus", "--run", hex_file], check=True)
            logger.success("Digispark flashé avec succès.")
            return {"status": "success", "hex": hex_file}
        except Exception as e:
            logger.error(f"Erreur flashage : {e}")
            return {"status": "error", "message": str(e)}

    def _flash_pico(self, bin_file):
        """Raspberry Pi Pico : copier sur le volume RPI-RP2 monté."""
        possible_mounts = ["/media/" + os.getlogin() + "/RPI-RP2", "/mnt/RPI-RP2", "/Volumes/RPI-RP2"]
        mount = next((m for m in possible_mounts if os.path.exists(m)), None)
        if not mount:
            logger.error("Pico non monté. Branchez-le en mode BOOTSEL.")
            return {"status": "error", "message": "Pico non détecté"}

        dest = os.path.join(mount, "payload.uf2")
        logger.info(f"Copie vers {dest}...")
        try:
            with open(bin_file, "rb") as src, open(dest, "wb") as dst:
                dst.write(src.read())
            logger.success("Pico flashé. Il va redémarrer.")
            return {"status": "success", "mount": mount}
        except Exception as e:
            logger.error(f"Erreur : {e}")
            return {"status": "error", "message": str(e)}

    def _flash_rubber_ducky(self, bin_file):
        """Rubber Ducky officiel : copier inject.bin sur la carte SD."""
        mount = None
        for m in ["/media/" + os.getlogin() + "/DUCKY", "/mnt/DUCKY"]:
            if os.path.exists(m):
                mount = m
                break

        if not mount:
            logger.error("Carte SD du Ducky non montée.")
            return {"status": "error", "message": "SD non détectée"}

        dest = os.path.join(mount, "inject.bin")
        try:
            with open(bin_file, "rb") as src, open(dest, "wb") as dst:
                dst.write(src.read())
            logger.success(f"inject.bin écrit sur {mount}")
            return {"status": "success", "sd_path": mount}
        except Exception as e:
            return {"status": "error", "message": str(e)}