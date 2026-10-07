"""
FOKARAT SDK - Classe de base pour tous les plugins
Tout plugin FOKARAT doit hériter de PluginBase.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PluginMetadata:
    """Métadonnées d'un plugin."""
    name: str
    version: str
    author: str
    description: str
    category: str = "general"  # payload, listener, injector, evasion, attack, misc
    tags: list = field(default_factory=list)
    requires_root: bool = False
    requires_scope: bool = False  # Nécessite une déclaration de scope


class PluginBase(ABC):
    """
    Classe de base pour tous les plugins FOKARAT.

    Exemple d'utilisation :
        from sdk import PluginBase, PluginMetadata

        class MyPlugin(PluginBase):
            @property
            def metadata(self):
                return PluginMetadata(
                    name="Mon Plugin",
                    version="1.0.0",
                    author="Moi",
                    description="Fait quelque chose",
                )

            def run(self, config, args=None):
                print("Hello from my plugin!")
                return {"status": "success"}
    """

    def __init__(self):
        self.logger = None  # Sera injecté par le loader

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Retourne les métadonnées du plugin."""
        pass

    @abstractmethod
    def run(self, config, args: Any = None) -> dict:
        """
        Exécute le plugin.

        Args:
            config: Instance de Config
            args: Arguments optionnels

        Returns:
            dict avec au moins {"status": "success" | "error"}
        """
        pass

    def validate(self) -> bool:
        """Validation optionnelle avant exécution."""
        return True

    def on_load(self) -> None:
        """Callback appelé au chargement du plugin."""
        pass

    def on_unload(self) -> None:
        """Callback appelé au déchargement du plugin."""
        pass

    def get_metadata_dict(self) -> dict:
        """Retourne les métadonnées sous forme de dictionnaire."""
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
        }