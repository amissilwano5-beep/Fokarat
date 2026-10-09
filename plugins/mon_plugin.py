# plugins/mon_plugin.py
from sdk import PluginBase, PluginMetadata

class MonPlugin(PluginBase):
    @property
    def metadata(self):
        return PluginMetadata(
            name="Mon Plugin",
            version="1.0.0",
            author="Votre Nom",
            description="Description",
            category="misc",
        )

    def run(self, config, args=None):
        print("Hello!")
        return {"status": "success"}