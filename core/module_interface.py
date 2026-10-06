"""
FOKARAT - Interface de module
Auteur: Lwano Amissi Blanchard (FOKAS)
Version: 1.0

Tous les modules de FOKARAT doivent hériter de ModuleInterface
et implémenter les méthodes get_metadata() et run().
"""

from abc import ABC, abstractmethod


class ModuleInterface(ABC):
    """
    Classe de base abstraite pour tous les modules FOKARAT.
    """

    @abstractmethod
    def get_metadata(self):
        """
        Retourne les métadonnées du module.
        Doit retourner un dict de la forme:
            {"name": "...", "version": "...", "type": "...", "description": "..."}
        """
        pass

    @abstractmethod
    def run(self, config):
        """
        Exécute le module avec la configuration donnée.
        Doit retourner un dict de la forme:
            {"status": "success" | "error", "message": "...", ...}
        """
        pass