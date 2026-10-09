"""
FOKARAT - Authentification JWT pour l'API
"""
import os
import hmac
import time
import base64
import hashlib
import json
import secrets

from fastapi import HTTPException, Header


class JWTManager:
    """
    Gestionnaire de tokens JWT (HMAC-SHA256).
    Utilise PyJWT si disponible, sinon fallback maison.
    """

    SECRET_FILE = "output/.jwt_secret"
    DEFAULT_EXPIRY = 3600  # 1h

    def __init__(self):
        self._secret = self._load_or_create_secret()
        self._backend = self._detect_backend()

    def _detect_backend(self):
        try:
            import jwt  # noqa
            return "pyjwt"
        except ImportError:
            return "fallback"

    def _load_or_create_secret(self):
        os.makedirs("output", exist_ok=True)
        if os.path.exists(self.SECRET_FILE):
            with open(self.SECRET_FILE, "rb") as f:
                return f.read()
        secret = secrets.token_bytes(64)
        with open(self.SECRET_FILE, "wb") as f:
            f.write(secret)
        try:
            os.chmod(self.SECRET_FILE, 0o600)
        except Exception:
            pass
        return secret

    def create_token(self, subject: str, expiry: int = None) -> str:
        expiry = expiry or self.DEFAULT_EXPIRY
        payload = {
            "sub": subject,
            "iat": int(time.time()),
            "exp": int(time.time()) + expiry,
        }

        if self._backend == "pyjwt":
            import jwt
            return jwt.encode(payload, self._secret, algorithm="HS256")

        # Fallback : implémentation maison
        header = {"alg": "HS256", "typ": "JWT"}
        h_b64 = self._b64url(json.dumps(header, separators=(",", ":")).encode())
        p_b64 = self._b64url(json.dumps(payload, separators=(",", ":")).encode())
        signature = self._sign(f"{h_b64}.{p_b64}")
        return f"{h_b64}.{p_b64}.{signature}"

    def verify_token(self, token: str) -> dict:
        try:
            if self._backend == "pyjwt":
                import jwt
                return jwt.decode(token, self._secret, algorithms=["HS256"])
            # Fallback
            parts = token.split(".")
            if len(parts) != 3:
                raise ValueError("Token invalide")
            h_b64, p_b64, sig = parts
            expected = self._sign(f"{h_b64}.{p_b64}")
            if not hmac.compare_digest(sig, expected):
                raise ValueError("Signature invalide")
            payload = json.loads(self._b64url_decode(p_b64))
            if payload.get("exp", 0) < time.time():
                raise ValueError("Token expiré")
            return payload
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Token invalide : {e}")

    def _sign(self, data: str) -> str:
        sig = hmac.new(self._secret, data.encode(), hashlib.sha256).digest()
        return self._b64url(sig)

    def _b64url(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

    def _b64url_decode(self, s: str) -> bytes:
        padding = "=" * (4 - len(s) % 4)
        return base64.urlsafe_b64decode(s + padding)


jwt_manager = JWTManager()


def require_auth(authorization: str = Header(default=None)):
    """
    Dépendance FastAPI : vérifie le header Authorization: Bearer <token>.
    Si FOKARAT_API_AUTH=0, désactive l'auth (mode dev).
    """
    if os.environ.get("FOKARAT_API_AUTH", "1") == "0":
        return {"sub": "anonymous", "dev_mode": True}

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header manquant")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Format : Bearer <token>")

    return jwt_manager.verify_token(parts[1])