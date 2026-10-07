"""
Plugin d'exemple : Hello World
Démontre comment créer un plugin FOKARAT.
"""
from sdk import PluginBase, PluginMetadata


class HelloWorldPlugin(PluginBase):
    """Plugin d'exemple qui affiche un message."""

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="Hello World",
            version="1.0.0",
            author="FOKAS",
            description="Plugin d'exemple pour tester le système de plugins.",
            category="misc",
            tags=["demo", "example"],
        )

    def run(self, config, args=None) -> dict:
        print("\n  👋 Hello from FOKARAT Plugin System!")
        print(f"  LHOST actuel : {config.get('lhost')}")
        print(f"  LPORT actuel : {config.get('lport')}")
        print()
        return {"status": "success", "message": "Hello World executed"}