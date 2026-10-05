import json
import datetime
import os
import sys

class Logger:
    def __init__(self, log_file: str = "framework.log", max_size_mb: int = 10):
        self.log_file = log_file
        self.max_size = max_size_mb * 1024 * 1024

    def _rotate(self):
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > self.max_size:
            backup = f"{self.log_file}.1"
            if os.path.exists(backup):
                os.remove(backup)
            os.rename(self.log_file, backup)

    def _write(self, level: str, msg: str, **kwargs):
        self._rotate()
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "level": level,
            "message": msg,
            **kwargs
        }
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
        if level in ("ERROR", "CRITICAL"):
            print(f"[{level}] {msg}", file=sys.stderr)

    def info(self, msg: str, **kwargs):
        self._write("INFO", msg, **kwargs)

    def error(self, msg: str, **kwargs):
        self._write("ERROR", msg, **kwargs)

    def debug(self, msg: str, **kwargs):
        self._write("DEBUG", msg, **kwargs)

    def warning(self, msg: str, **kwargs):
        self._write("WARNING", msg, **kwargs)