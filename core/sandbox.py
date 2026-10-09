"""
FOKARAT - Sandbox d'exécution
Limite les ressources des processus lancés (CPU, RAM, temps).
"""
import os
import sys
import time
import subprocess
import resource
from contextlib import contextmanager

from core.logger import Logger

logger = Logger()


class Sandbox:
    """
    Sandbox pour l'exécution de commandes externes.
    Limite CPU, RAM, et durée d'exécution.
    """

    DEFAULTS = {
        "cpu_seconds": 60,
        "memory_mb": 512,
        "max_processes": 20,
        "timeout": 120,
        "max_output_kb": 1024,
    }

    def __init__(self, limits=None):
        self.limits = {**self.DEFAULTS, **(limits or {})}

    def _apply_limits(self):
        """Applique les limites au processus courant (à appeler dans preexec_fn)."""
        cpu = self.limits["cpu_seconds"]
        mem = self.limits["memory_mb"] * 1024 * 1024
        nproc = self.limits["max_processes"]

        try:
            resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))
            resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
            resource.setrlimit(resource.RLIMIT_NPROC, (nproc, nproc))
            resource.setrlimit(resource.RLIMIT_FSIZE,
                               (self.limits["max_output_kb"] * 1024 * 1024,) * 2)
        except (ValueError, OSError) as e:
            logger.warning(f"Impossible d'appliquer certaines limites : {e}")

    def run(self, cmd, cwd=None, env=None, timeout=None):
        """
        Exécute une commande dans le sandbox.
        Retourne dict {status, stdout, stderr, returncode, duration}.
        """
        if isinstance(cmd, str):
            cmd = cmd.split()

        timeout = timeout or self.limits["timeout"]
        start = time.time()

        # preexec_fn est UNIX-only
        preexec = self._apply_limits if os.name == "posix" else None

        try:
            proc = subprocess.run(
                cmd,
                cwd=cwd,
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout,
                preexec_fn=preexec,
            )
            duration = time.time() - start

            result = {
                "status": "success" if proc.returncode == 0 else "error",
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "returncode": proc.returncode,
                "duration": round(duration, 3),
            }

            if proc.returncode != 0:
                logger.warning(f"Commande terminée avec code {proc.returncode} en {duration:.2f}s")
            else:
                logger.success(f"Commande terminée en {duration:.2f}s")

            return result

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout dépassé ({timeout}s)")
            return {
                "status": "timeout",
                "stdout": "",
                "stderr": "",
                "returncode": -1,
                "duration": round(time.time() - start, 3),
            }
        except FileNotFoundError as e:
            logger.error(f"Commande introuvable : {e}")
            return {
                "status": "error",
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "duration": 0,
            }
        except Exception as e:
            logger.error(f"Erreur sandbox : {e}")
            return {
                "status": "error",
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "duration": round(time.time() - start, 3),
            }

    @contextmanager
    def isolated_cwd(self, path):
        """Context manager qui change de dossier temporairement."""
        old = os.getcwd()
        try:
            os.chdir(path)
            yield
        finally:
            os.chdir(old)

    def is_available(self) -> bool:
        """Indique si le sandbox complet est disponible."""
        return os.name == "posix" and hasattr(resource, "setrlimit")