"""
FOKARAT - Chiffrement AES-256 des secrets
Protège les clés, tokens et mots de passe stockés.
"""
import os
import base64
import json
import hashlib

from core.logger import Logger

logger = Logger()


class CryptoManager:
    """
    Gestionnaire de chiffrement AES-256-GCM.
    Utilise la librairie cryptography si disponible, sinon fallback XOR+SHA256.
    """

    KEY_FILE = "output/.fokarat_key"
    SALT_SIZE = 16
    NONCE_SIZE = 12

    def __init__(self):
        self._key = self._load_or_create_key()
        self._backend = self._detect_backend()

    def _detect_backend(self):
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            return "aesgcm"
        except ImportError:
            logger.warning("cryptography absent, fallback XOR-SHA256 (moins sécurisé)")
            return "fallback"

    def _load_or_create_key(self):
        """Charge ou génère la clé maître."""
        os.makedirs("output", exist_ok=True)
        if os.path.exists(self.KEY_FILE):
            with open(self.KEY_FILE, "rb") as f:
                return f.read()
        key = os.urandom(32)
        with open(self.KEY_FILE, "wb") as f:
            f.write(key)
        try:
            os.chmod(self.KEY_FILE, 0o600)
        except Exception:
            pass
        logger.success(f"Clé maître créée : {self.KEY_FILE}")
        return key

    def _derive_key(self, salt):
        return hashlib.pbkdf2_hmac("sha256", self._key, salt, 100_000, dklen=32)

    def encrypt(self, plaintext: str) -> str:
        """Chiffre une chaîne et retourne un blob base64."""
        if not isinstance(plaintext, str):
            plaintext = json.dumps(plaintext)
        data = plaintext.encode("utf-8")
        salt = os.urandom(self.SALT_SIZE)
        derived = self._derive_key(salt)

        if self._backend == "aesgcm":
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            nonce = os.urandom(self.NONCE_SIZE)
            aes = AESGCM(derived)
            ct = aes.encrypt(nonce, data, None)
            blob = salt + nonce + ct
        else:
            # Fallback : XOR avec keystream SHA256
            stream = self._keystream(derived, len(data))
            ct = bytes(a ^ b for a, b in zip(data, stream))
            blob = salt + ct

        return base64.b64encode(blob).decode("ascii")

    def decrypt(self, blob: str) -> str:
        """Déchiffre un blob base64."""
        raw = base64.b64decode(blob)
        salt = raw[: self.SALT_SIZE]
        derived = self._derive_key(salt)

        if self._backend == "aesgcm":
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            nonce = raw[self.SALT_SIZE : self.SALT_SIZE + self.NONCE_SIZE]
            ct = raw[self.SALT_SIZE + self.NONCE_SIZE :]
            aes = AESGCM(derived)
            pt = aes.decrypt(nonce, ct, None)
        else:
            ct = raw[self.SALT_SIZE :]
            stream = self._keystream(derived, len(ct))
            pt = bytes(a ^ b for a, b in zip(ct, stream))

        return pt.decode("utf-8")

    def _keystream(self, key, length):
        """Génère un keystream déterministe à partir de la clé."""
        out = b""
        counter = 0
        while len(out) < length:
            out += hashlib.sha256(key + counter.to_bytes(8, "big")).digest()
            counter += 1
        return out[:length]

    def encrypt_file(self, filepath: str) -> bool:
        """Chiffre un fichier entier (remplace le contenu)."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            encrypted = self.encrypt(content)
            with open(filepath + ".enc", "w", encoding="utf-8") as f:
                f.write(encrypted)
            logger.success(f"Chiffré : {filepath}.enc")
            return True
        except Exception as e:
            logger.error(f"Erreur chiffrement fichier : {e}")
            return False

    def decrypt_file(self, filepath: str) -> str:
        """Déchiffre un fichier .enc et retourne le contenu."""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return self.decrypt(content)

    def get_backend(self):
        return self._backend