"""
FOKARAT - API REST Stable v2.0
- Sécurité par variables d'environnement OBLIGATOIRES
- Vérification de scope sur tous les endpoints sensibles
- Chiffrement JWT
"""
import os
import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.auth import require_auth, jwt_manager
from web.webhooks import webhook_manager

app = FastAPI(
    title="FOKARAT API",
    version="2.0.0",
    description="API REST sécurisée pour piloter FOKARAT.",
    contact={"name": "Lwano Amissi Blanchard (FOKAS)", "email": "amissilwano5@gmail.com"},
    license_info={"name": "MIT"},
)


# ══════════════════════════════════════════════════
#  VÉRIFICATION DES VARIABLES D'ENVIRONNEMENT
# ══════════════════════════════════════════════════
def _check_env_security():
    """Refuse de démarrer si les identifiants par défaut sont utilisés."""
    user = os.environ.get("FOKARAT_API_USER")
    pwd = os.environ.get("FOKARAT_API_PASS")

    if not user or not pwd:
        print("=" * 70)
        print("  ❌ ERREUR : Variables d'environnement manquantes")
        print("=" * 70)
        print()
        print("  FOKARAT refuse de démarrer sans identifiants sécurisés.")
        print()
        print("  Avant de lancer l'API, définissez :")
        print()
        print("    export FOKARAT_API_USER='votre_username'")
        print("    export FOKARAT_API_PASS='mot_de_passe_fort'")
        print()
        print("  Puis relancez FOKARAT.")
        print("=" * 70)
        sys.exit(1)

    if len(pwd) < 12:
        print("=" * 70)
        print("  ⚠️  ATTENTION : Mot de passe trop court")
        print("=" * 70)
        print("  Le mot de passe doit contenir au moins 12 caractères.")
        sys.exit(1)


# ══════════════════════════════════════════════════
#  MODÈLES
# ══════════════════════════════════════════════════
class TokenRequest(BaseModel):
    username: str
    password: str


class PayloadRequest(BaseModel):
    type: str
    lhost: str
    lport: int = Field(..., ge=1, le=65535)


class ScopeRequest(BaseModel):
    target: str
    auth_ref: str
    hours: int = Field(24, ge=1, le=168)


class MitreRequest(BaseModel):
    actions: list


class WebhookRequest(BaseModel):
    url: str


# ══════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════
def _require_active_scope():
    """Vérifie qu'un scope actif existe. Lève 403 sinon."""
    from core.scope import ScopeValidator
    scope = ScopeValidator().load_scope()
    if not scope:
        raise HTTPException(
            status_code=403,
            detail="Aucun scope actif. Déclarez un scope via POST /scope/declare.",
        )
    return scope


def _check_target_in_scope(target: str):
    """Vérifie que la cible est bien dans le scope actif."""
    scope = _require_active_scope()
    if scope["target"] != target:
        raise HTTPException(
            status_code=403,
            detail=f"Cible '{target}' non autorisée. Scope actif : '{scope['target']}'.",
        )
    return scope


# ══════════════════════════════════════════════════
#  AUTH
# ══════════════════════════════════════════════════
@app.post("/auth/token", tags=["Auth"])
def get_token(req: TokenRequest):
    """Génère un token JWT."""
    expected_user = os.environ.get("FOKARAT_API_USER")
    expected_pass = os.environ.get("FOKARAT_API_PASS")

    if req.username != expected_user or req.password != expected_pass:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = jwt_manager.create_token(req.username, expiry=3600)
    return {"access_token": token, "token_type": "bearer", "expires_in": 3600}


# ══════════════════════════════════════════════════
#  STATUS (public)
# ══════════════════════════════════════════════════
@app.get("/", tags=["Status"])
def root():
    return {
        "framework": "FOKARAT",
        "version": "3.5.0",
        "api_version": "2.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/health", tags=["Status"])
def health():
    return {"status": "ok"}


# ══════════════════════════════════════════════════
#  SCOPE (protégé)
# ══════════════════════════════════════════════════
@app.post("/scope/declare", tags=["Scope"])
def declare_scope(req: ScopeRequest, _=Depends(require_auth)):
    import json, datetime
    from core.scope import ScopeValidator
    sv = ScopeValidator()

    scope = {
        "target": req.target,
        "auth_ref": req.auth_ref,
        "created_at": datetime.datetime.utcnow().isoformat(),
        "expires_at": (datetime.datetime.utcnow() +
                       datetime.timedelta(hours=req.hours)).isoformat(),
        "hours": req.hours,
    }
    os.makedirs("output", exist_ok=True)
    with open(sv.SCOPE_FILE, "w") as f:
        json.dump(scope, f, indent=2)

    webhook_manager.emit("scope.declared", {"target": req.target})
    return {"status": "success", "scope": scope}


@app.get("/scope/active", tags=["Scope"])
def get_active_scope(_=Depends(require_auth)):
    from core.scope import ScopeValidator
    scope = ScopeValidator().load_scope()
    return {"active": bool(scope), "scope": scope}


# ══════════════════════════════════════════════════
#  PAYLOADS (protégé + scope vérifié)
# ══════════════════════════════════════════════════
@app.post("/payload/python", tags=["Payloads"])
def gen_python(req: PayloadRequest, _=Depends(require_auth)):
    if req.type != "python":
        raise HTTPException(400, "type doit être 'python'")
    _check_target_in_scope(req.lhost)  # ← SCOPE OBLIGATOIRE

    from core.config import Config
    from modules.payload_generators.python_gen import PythonPayloadGenerator
    cfg = Config()
    cfg.set("lhost", req.lhost)
    cfg.set("lport", req.lport)

    result = PythonPayloadGenerator().run(cfg)
    webhook_manager.emit("payload.generated", {"type": "python", "lhost": req.lhost})
    return result


@app.post("/payload/cpp", tags=["Payloads"])
def gen_cpp(req: PayloadRequest, _=Depends(require_auth)):
    if req.type != "cpp":
        raise HTTPException(400, "type doit être 'cpp'")
    _check_target_in_scope(req.lhost)

    from core.config import Config
    from modules.payload_generators.cpp_gen import CppPayloadGenerator
    cfg = Config()
    cfg.set("lhost", req.lhost)
    cfg.set("lport", req.lport)
    return CppPayloadGenerator().run(cfg)


@app.post("/payload/msfvenom", tags=["Payloads"])
def gen_msfvenom(req: PayloadRequest, _=Depends(require_auth)):
    if req.type != "msfvenom":
        raise HTTPException(400, "type doit être 'msfvenom'")
    _check_target_in_scope(req.lhost)

    from core.config import Config
    from modules.payload_generators.msfvenom_gen import MsfvenomGenerator
    cfg = Config()
    cfg.set("lhost", req.lhost)
    cfg.set("lport", req.lport)
    return MsfvenomGenerator().run(cfg)


@app.get("/payloads", tags=["Payloads"])
def list_payloads(_=Depends(require_auth)):
    from core.database import Database
    return {"payloads": Database().get_all_payloads()}


# ══════════════════════════════════════════════════
#  RAPPORTS (protégé)
# ══════════════════════════════════════════════════
@app.get("/report", tags=["Reports"])
def report(_=Depends(require_auth)):
    from core.database import Database
    path = Database().export_report()
    with open(path, encoding="utf-8") as f:
        return {"report": f.read(), "path": path}


@app.post("/report/mitre", tags=["Reports"])
def report_mitre(req: MitreRequest, _=Depends(require_auth)):
    from core.mitre import MitreMapper
    return {"report": MitreMapper().generate_report(req.actions)}


# ══════════════════════════════════════════════════
#  WEBHOOKS (protégé)
# ══════════════════════════════════════════════════
@app.post("/webhooks/add", tags=["Webhooks"])
def add_webhook(req: WebhookRequest, _=Depends(require_auth)):
    webhook_manager.add_hook(req.url)
    return {"status": "success", "hooks": webhook_manager.hooks}


@app.get("/webhooks/list", tags=["Webhooks"])
def list_webhooks(_=Depends(require_auth)):
    return {"hooks": webhook_manager.hooks}


# ══════════════════════════════════════════════════
#  LANCEMENT
# ══════════════════════════════════════════════════
@app.on_event("startup")
def startup():
    _check_env_security()
    webhook_manager.start()


@app.on_event("shutdown")
def shutdown():
    webhook_manager.stop()


def start_web(host="127.0.0.1", port=5000):
    import uvicorn
    uvicorn.run(app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    start_web()