import os
from core.logger import Logger

logger = Logger()

class Assistant:
    def __init__(self, model_path="models/mistral-7b.gguf"):
        self.model_path = model_path
        self.llm = None
        self.context = []
        self._load_model()

    def _load_model(self):
        try:
            from llama_cpp import Llama
            if os.path.exists(self.model_path):
                self.llm = Llama(model_path=self.model_path, n_ctx=4096, n_threads=4, verbose=False)
                logger.info("Assistant IA chargé")
            else:
                logger.error(f"Modèle introuvable : {self.model_path}")
        except Exception as e:
            logger.error(f"Erreur chargement modèle : {e}")

    def chat(self, user_message):
        if not self.llm:
            return "Modèle non chargé. Vérifie le chemin."

        system_prompt = (
            "Tu es un assistant expert en cybersécurité offensive, spécialisé dans le framework Doctoral. "
            "Tu aides l'utilisateur à générer des payloads, configurer des listeners, éviter les antivirus, "
            "et comprendre les techniques avancées. Réponds de manière claire et technique."
        )

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.context[-5:])
        messages.append({"role": "user", "content": user_message})

        prompt = ""
        for msg in messages:
            prompt += f"{msg['role']}: {msg['content']}\n"
        prompt += "assistant:"

        try:
            output = self.llm(prompt, max_tokens=512, temperature=0.7, stop=["user:", "assistant:"])
            reply = output['choices'][0]['text'].strip()
            self.context.append({"role": "user", "content": user_message})
            self.context.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            logger.error(f"Erreur lors de l'inférence : {e}")
            return "Je rencontre un problème technique."