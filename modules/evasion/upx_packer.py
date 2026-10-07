"""
FOKARAT - Compression UPX automatique
Réduit la taille des binaires et modifie les signatures.
"""
import os
import subprocess
from core.logger import Logger
from core.utils import which

logger = Logger()


class UPXPacker:

    def pack(self, binary_path, ultra=True):
        if not which("upx"):
            logger.warning("UPX non installé. sudo apt install upx-ucl")
            return binary_path

        if not os.path.exists(binary_path):
            logger.error(f"Binaire introuvable : {binary_path}")
            return binary_path

        out_path = binary_path + ".packed"
        args = ["upx"]
        if ultra:
            args.append("--ultra-brute")
        args += ["-f", "-o", out_path, binary_path]

        logger.info(f"Compression UPX : {os.path.basename(binary_path)}")

        try:
            result = subprocess.run(args, check=True, capture_output=True, text=True)
            size_orig = os.path.getsize(binary_path)
            size_new = os.path.getsize(out_path)
            ratio = (1 - size_new / size_orig) * 100
            logger.success(
                f"UPX : {size_orig//1024} Ko -> {size_new//1024} Ko (-{ratio:.1f}%)"
            )

            # Remplace l'original par la version packée
            os.replace(out_path, binary_path)
            return binary_path

        except subprocess.CalledProcessError as e:
            logger.error(f"UPX échoué : {e.stderr or e}")
            if os.path.exists(out_path):
                os.remove(out_path)
            return binary_path