"""
FOKARAT SDK - Classe de base pour tous les plugins
Le scope est appliqué PAR DÉFAUT pour tout plugin qui le requiert.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class ScopeError(Exception):
    """Erreur levée si le scope est invalide ou manquant."""
    pass


@dataclass
class PluginMetadata:
    """Métadonnées d'un plugin."""
    name: str
    version: str
    author: str
    description: str
    category: str = "general"
    tags: list = field(default_factory=list)
    requires_root: bool = False
    requires_scope: bool = False
    target_param: str = "target"  # Nom du paramètre contenant la cible


class PluginBase(ABC):
    """
    Classe de base pour tous les plugins FOKARAT.

    IMPORTANT : Si `requires_scope=True` dans les métadonnées,
    la méthode `run()` VÉRIFIE automatiquement que la cible
    est bien dans le scope actif. Sinon, elle lève `ScopeError`.
    """

    def __init__(self):
        self.logger = None

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Retourne les métadonnées du plugin."""
        pass

    @abstractmethod
    def _execute(self, config, args: Any = None) -> dict:
        """
        Logique interne du plugin.
        Ne pas appeler directement. Utiliser run().
        """
        pass

    def run(self, config, args: Any = None) -> dict:
        """
        Point d'entrée public. Applique les vérifications de scope.
        """
        # Vérification du scope si requis
        if self.metadata.requires_scope:
            self._enforce_scope(config, args)

        # Exécution interne
        return self._execute(config, args)

    def _enforce_scope(self, config, args):
        """Force la présence d'un scope valide et vérifie la cible."""
        from core.scope import ScopeValidator

        # Récupère le scope actif
        sv = ScopeValidator()
        scope = sv.load_scope()

        if not scope:
            raise ScopeError(
                f"Plugin '{self.metadata.name}' requiert un scope actif. "
                "Déclarez un scope avec [30] avant de l'exécuter."
            )

        # Extrait la cible depuis args
        target = None
        if args and isinstance(args, dict):
            target = args.get(self.metadata.target_param)
        elif args and hasattr(args, self.metadata.target_param):
            target = getattr(args, self.metadata.target_param)

        if not target:
            raise ScopeError(
                f"Plugin '{self.metadata.name}' requiert le paramètre "
                f"'{self.metadata.target_param}' pour vérifier le scope."
            )

        # Vérifie que la cible est dans le scope
        if scope["target"] != target:
            raise ScopeError(
                f"Cible '{target}' NON AUTORISÉE. "
                f"Le scope actif est '{scope['target']}'."
            )

        self._log_scope_check(target, scope)
        return True

    def _log_scope_check(self, target, scope):
        """Log l'utilisation du scope."""
        try:
            from core.ethics import EthicsController
            EthicsController().audit(
                "SCOPE_CHECKED",
                f"plugin={self.metadata.name} target={target} scope={scope['target']}"
            )
        except Exception:
            pass

    def validate(self) -> bool:
        """Validation optionnelle."""
        return True

    def on_load(self) -> None:
        """Callback au chargement."""
        pass

    def on_unload(self) -> None:
        """Callback au déchargement."""
        pass

    def get_metadata_dict(self) -> dict:
        m = self.metadata
        return {
            "name": m.name,
            "version": m.version,
            "author": m.author,
            "description": m.description,
            "category": m.category,
            "tags": m.tags,
            "requires_root": m.requires_root,
            "requires_scope": m.requires_scope,
            "target_param": m.target_param,
        }