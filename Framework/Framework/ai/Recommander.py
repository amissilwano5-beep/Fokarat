from core.config import Config

class Recommender:
    def __init__(self):
        self.config = Config()

    def suggest_payload(self, target_os="Windows", is_sandbox=False):
        if target_os == "Windows":
            if is_sandbox:
                return {
                    "payload": "Python SSL",
                    "reason": "Sandbox détectée, Python plus furtif et modifiable",
                    "port": 4444
                }
            else:
                return {
                    "payload": "C++ syscalls",
                    "reason": "Meilleure résistance aux AV, appels directs au noyau",
                    "port": 4444
                }
        else:
            return {
                "payload": "Python SSL",
                "reason": "Non-Windows, Python multi-plateforme",
                "port": 4444
            }