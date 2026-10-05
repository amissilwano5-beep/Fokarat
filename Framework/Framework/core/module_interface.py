from abc import ABC, abstractmethod
from typing import Any, Dict


class ModuleInterface(ABC):
    @abstractmethod
    def run(self, config: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        pass


__all__ = ["ModuleInterface"]
