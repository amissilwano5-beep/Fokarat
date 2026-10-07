"""
FOKARAT - Contrôles éthiques
Kill switch, mode dry-run, journal d'audit.
"""
import os
import json
import signal
import datetime
from core.logger import Logger

logger = Logger()


class EthicsController:
    """
    Contrôle éthique du framework :
    - Kill switch (arrêt d'urgence)
    - Dry-run (simulation)
    - Journal d'audit
    """

    AUDIT_LOG = "output/audit.log"

    def __init__(self):
        self.dry_run = False
        self.killed = False
        os.makedirs("output", exist_ok=True)

        # Installation du kill switch
        signal.signal(signal.SIGINT, self._emergency_stop_handler)
        signal.signal(signal.SIGTERM, self._emergency_stop_handler)

    def _emergency_stop_handler(self, signum, frame):
        """Kill switch : arrête tout immédiatement."""
        self.killed = True
        logger.error("\n🚨 KILL SWITCH ACTIVÉ — Arrêt d'urgence")
        self.audit("KILL_SWITCH", "Arrêt d'urgence déclenché")
        raise SystemExit(1)

    def enable_dry_run(self):
        """Active le mode simulation."""
        self.dry_run = True
        logger.warning("Mode DRY-RUN activé : aucune action réelle ne sera exécutée")
        self.audit("DRY_RUN", "Mode simulation activé")

    def disable_dry_run(self):
        self.dry_run = False
        logger.info("Mode DRY-RUN désactivé")
        self.audit("DRY_RUN", "Mode simulation désactivé")

    def audit(self, action, details=""):
        """Enregistre une action dans le journal d'audit."""
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "action": action,
            "details": details,
            "dry_run": self.dry_run,
        }
        try:
            with open(self.AUDIT_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def confirm_action(self, action_description):
        """Demande une double confirmation pour les actions sensibles."""
        if self.dry_run:
            logger.info(f"[DRY-RUN] {action_description}")
            return True

        print(f"\n  ⚠️  Action sensible : {action_description}")
        confirm = input("  [>] Confirmer ? (oui/non) : ").strip().lower()
        if confirm == "oui":
            self.audit("ACTION_CONFIRMED", action_description)
            return True
        logger.warning("Action annulée par l'utilisateur.")
        self.audit("ACTION_CANCELLED", action_description)
        return False