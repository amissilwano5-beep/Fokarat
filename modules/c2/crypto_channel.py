"""
FOKARAT - Chiffrement du canal C2
AES-256-GCM avec dérivation de clé par session.
"""
import os
import base64
import hashlib
import secrets


class C2Crypto:
    """
    Chiffrement du canal C2.
    AES-256-GCM si cryptography dispo, sinon ChaCha20-Poly1305-like en pure Python.
    """

    KEY_SIZE = 32
    NONCE_SIZE = 12

    def __init__(self, session_key: bytes = None):
        self.session_key = session_key or secrets.token_bytes(self.KEY_SIZE)
        self._backend = self._detect_backend()

    def _detect_backend(self):
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            return "aesgcm"
        except ImportError:
            return "xchacha"

    def derive_key(self, password: str, salt: bytes = None) -> bytes:
        """Dérive une clé depuis un password (PBKDF2)."""
        salt = salt or secrets.token_bytes(16)
        return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000, dklen=self.KEY_SIZE), salt

    def encrypt(self, plaintext: bytes) -> bytes:
        """Chiffre et retourne nonce + ciphertext + tag."""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode("utf-8")

        nonce = secrets.token_bytes(self.NONCE_SIZE)

        if self._backend == "aesgcm":
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            aes = AESGCM(self.session_key)
            ct = aes.encrypt(nonce, plaintext, None)
            return nonce + ct

        # Fallback : XOR + HMAC
        keystream = self._keystream(nonce, len(plaintext))
        ct = bytes(a ^ b for a, b in zip(plaintext, keystream))
        tag = hashlib.sha256(self.session_key + nonce + ct).digest()[:16]
        return nonce + tag + ct

    def decrypt(self, blob: bytes) -> bytes:
        """Déchiffre un blob (nonce + ciphertext)."""
        nonce = blob[:self.NONCE_SIZE]

        if self._backend == "aesgcm":
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            aes = AESGCM(self.session_key)
            ct = blob[self.NONCE_SIZE:]
            return aes.decrypt(nonce, ct, None)

        # Fallback
        tag = blob[self.NONCE_SIZE:self.NONCE_SIZE + 16]
        ct = blob[self.NONCE_SIZE + 16:]
        expected = hashlib.sha256(self.session_key + nonce + ct).digest()[:16]
        if tag != expected:
            raise ValueError("Tag invalide")
        keystream = self._keystream(nonce, len(ct))
        return bytes(a ^ b for a, b in zip(ct, keystream))

    def encrypt_str(self, s: str) -> str:
        """Chiffre une chaîne et retourne en base64."""
        return base64.b64encode(self.encrypt(s)).decode("ascii")

    def decrypt_str(self, b64: str) -> str:
        """Déchiffre une chaîne base64."""
        return self.decrypt(base64.b64decode(b64)).decode("utf-8")

    def _keystream(self, nonce: bytes, length: int) -> bytes:
        """Génère un keystream déterministe."""
        out = b""
        counter = 0
        while len(out) < length:
            block = hashlib.sha256(self.session_key + nonce + counter.to_bytes(8, "big")).digest()
            out += block
            counter += 1
        return out[:length]

    def get_backend(self) -> str:
        return self._backend