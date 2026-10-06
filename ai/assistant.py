"""FOKARAT - Assistant IA local (optionnel)"""
import os
from core.logger import Logger

logger = Logger()


class Assistant:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.llm = None

    def _load(self):
        if self.llm is not None:
            return True
        if not self.model_path or not os.path.exists(self.model_path):
            return False
        try:
            from llama_cpp import Llama
            self.llm = Llama(model_path=self.model_path, n_ctx=2048, verbose=False)
            return True
        except Exception as e:
            logger.warning(f"IA locale indisponible : {e}")
            return False

    def chat(self, question):
        if not self._load():
            return "[!] L'IA locale n'est pas disponible. Installez llama-cpp-python et téléchargez un modèle GGUF."
        try:
            out = self.llm(f"Q: {question}\nA:", max_tokens=256, stop=["Q:", "\n"])
            return out["choices"][0]["text"].strip()
        except Exception as e:
            return f"[!] Erreur IA : {e}"