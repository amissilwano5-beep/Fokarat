"""
FOKARAT - Encodeur DuckyScript -> .bin
Compile un script .duck en binaire pour Digispark / Rubber Ducky.
"""
import os
import subprocess
from core.module_interface import ModuleInterface
from core.logger import Logger
from core.utils import ensure_dir, which, safe_input

logger = Logger()


class DuckEncoder(ModuleInterface):
    def get_metadata(self):
        return {
            "name": "DuckEncoder",
            "version": "1.0",
            "type": "encoder",
            "description": "Compile un .duck en .bin pour matériel BadUSB."
        }

    def run(self, config):
        duck_file = safe_input("  [>] Chemin du fichier .duck : ").strip()
        if not os.path.exists(duck_file):
            logger.error("Fichier .duck introuvable.")
            return {"status": "error", "message": "Fichier introuvable"}

        out_dir = ensure_dir(config.get("output_dir", "output"))
        bin_file = os.path.join(out_dir, os.path.basename(duck_file).replace(".duck", ".bin"))

        # Méthode 1 : via duckencoder.jar (Java)
        if which("java"):
            jar = self._find_duckencoder_jar()
            if jar:
                logger.info(f"Compilation via {jar}...")
                try:
                    subprocess.run(
                        ["java", "-jar", jar, "-i", duck_file, "-o", bin_file],
                        check=True, capture_output=True
                    )
                    logger.success(f"Binaire généré : {bin_file}")
                    return {"status": "success", "bin_path": bin_file}
                except subprocess.CalledProcessError as e:
                    logger.warning(f"Échec duckencoder : {e}")

        # Méthode 2 : via Python (duckencoder.py)
        try:
            import duckencoder
            logger.info("Compilation via duckencoder Python...")
            with open(duck_file) as f:
                script = f.read()
            binary = duckencoder.encode_script(script)
            with open(bin_file, "wb") as f:
                f.write(binary)
            logger.success(f"Binaire généré : {bin_file}")
            return {"status": "success", "bin_path": bin_file}
        except ImportError:
            pass

        # Méthode 3 : télécharger duckencoder.jar si absent
        logger.warning("Aucun encodeur trouvé. Téléchargement de duckencoder.jar...")
        jar_url = "https://github.com/hak5darren/USB-Rubber-Ducky/raw/master/Encoder/duckencoder.jar"
        jar_path = "tools/duckencoder.jar"
        ensure_dir("tools")

        try:
            import urllib.request
            urllib.request.urlretrieve(jar_url, jar_path)
            logger.success(f"Téléchargé : {jar_path}")

            if which("java"):
                subprocess.run(
                    ["java", "-jar", jar_path, "-i", duck_file, "-o", bin_file],
                    check=True, capture_output=True
                )
                logger.success(f"Binaire généré : {bin_file}")
                return {"status": "success", "bin_path": bin_file}
        except Exception as e:
            logger.error(f"Impossible de compiler : {e}")
            return {"status": "error", "message": "Encodeur indisponible"}

    def _find_duckencoder_jar(self):
        candidates = ["tools/duckencoder.jar", "duckencoder.jar", os.path.expanduser("~/duckencoder.jar")]
        for c in candidates:
            if os.path.exists(c):
                return c
        return None