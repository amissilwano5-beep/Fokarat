"""
FOKARAT - Validation de scope
Vérifie que l'utilisateur a l'autorisation avant chaque attaque.
"""
import os
import json
import datetime
from core.logger import Logger

logger = Logger()


class ScopeValidator:
    """
    Force l'utilisateur à déclarer son scope et à confirmer
    qu'il a l'autorisation écrite avant toute action offensive.
    """

    SCOPE_FILE = "output/active_scope.json"

    def __init__(self):
        os.makedirs("output", exist_ok=True)
        self.active_scope = None

    def _ask_confirmation(self):
        print("\n" + "=" * 60)
        print("  ⚠️  DÉCLARATION DE SCOPE OBLIGATOIRE")
        print("=" * 60)
        print("\n  Avant toute action offensive, vous devez :")
        print("  1. Avoir une autorisation ÉCRITE du propriétaire")
        print("  2. Déclarer précisément la cible")
        print("  3. Confirmer votre identité\n")

        target = input("  [>] Cible (IP / domaine) : ").strip()
        if not target:
            logger.error("Cible obligatoire.")
            return None

        auth_ref = input("  [>] Référence de l'autorisation (email, contrat) : ").strip()
        if not auth_ref:
            logger.error("Référence d'autorisation obligatoire.")
            return None

        duration = input("  [>] Durée d'autorisation (heures) [24] : ").strip()
        try:
            hours = int(duration) if duration else 24
        except ValueError:
            hours = 24

        print("\n  Vous certifiez sur l'honneur que :")
        print(f"    ✓ Vous avez l'autorisation ÉCRITE pour cibler {target}")
        print(f"    ✓ Vous êtes dans un cadre LÉGAL")
        print(f"    ✓ Vous assumez l'entière responsabilité")

        confirm = input("\n  [>] Tapez 'JE CERTIFIE' pour continuer : ").strip()

        if confirm != "JE CERTIFIE":
            logger.error("Confirmation refusée. Action annulée.")
            return None

        scope = {
            "target": target,
            "auth_ref": auth_ref,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "expires_at": (datetime.datetime.utcnow() +
                          datetime.timedelta(hours=hours)).isoformat(),
            "hours": hours,
        }

        with open(self.SCOPE_FILE, "w", encoding="utf-8") as f:
            json.dump(scope, f, indent=2)

        self.active_scope = scope
        logger.success(f"Scope validé pour {target} (expire dans {hours}h)")
        return scope

    def load_scope(self):
        """Charge un scope actif s'il existe."""
        if os.path.exists(self.SCOPE_FILE):
            try:
                with open(self.SCOPE_FILE, "r", encoding="utf-8") as f:
                    scope = json.load(f)
                expires = datetime.datetime.fromisoformat(scope["expires_at"])
                if datetime.datetime.utcnow() < expires:
                    self.active_scope = scope
                    return scope
                else:
                    logger.warning("Scope expiré. Revalidation requise.")
                    os.remove(self.SCOPE_FILE)
            except Exception:
                pass
        return None

    def require_scope(self):
        """Oblige à avoir un scope valide avant toute action."""
        scope = self.load_scope()
        if scope:
            logger.info(f"Scope actif : {scope['target']}")
            return scope
        return self._ask_confirmation()

    def check_target(self, target):
        """Vérifie que la cible est dans le scope."""
        if not self.active_scope:
            return False
        return self.active_scope["target"] == target