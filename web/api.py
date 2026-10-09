"""
FOKARAT - API REST Stable v1.1
Auth JWT + Webhooks + MITRE
"""
import os
import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.auth import require_auth, jwt_manager
from web.webhooks import webhook_manager

app = FastAPI(
    title="FOKARAT API",
    version="1.1.0",
    description="API REST sécurisée pour piloter FOKARAT.",
    contact={"name": "Lwano Amissi Blanchard (FOKAS)", "email": "amissilwano5@gmail.com"},
    license_info={"name": "MIT"},
)


# ══════════════════════════════════════════════════
#  MODÈLES
# ══════════════════════════════════════════════════
class PayloadRequest(BaseModel):
    type: str = Field(..., description="python, cpp, msfvenom")
    lhost: str
    lport: int = Field(..., ge=1, le=65535)


class ScopeRequest(BaseModel):
    target: str
    auth_ref: str
    hours: int = Field(24, ge=1, le=168)


class MitreRequest(BaseModel):
    actions: list


class TokenRequest(BaseModel):
    username: str
    password: str


class WebhookRequest(BaseModel):
    url: str


# ══════════════════════════════════════════════════
#  AUTH
# ══════════════════════════════════════════════════
@app.post("/auth/token", tags=["Auth"])
def get_token(req: TokenRequest):
    """
    Génère un token JWT.
    Utilise FOKARAT_API_USER / FOKARAT_API_PASS (env).
    Défaut : admin / fokarat
    """
    expected_user = os.environ.get("FOKARAT_API_USER", "admin")
    expected_pass = os.environ.get("FOKARAT_API_PASS", "fokarat")

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
        "version": "3.4.0",
        "api_version": "1.1.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/health", tags=["Status"])
def health():
    return {"status": "ok"}


@app.get("/version", tags=["Status"])
def version():
    return {"fokarat": "3.4.0", "api": "1.1.0", "python": sys.version.split()[0]}


# ══════════════════════════════════════════════════
#  PAYLOADS (protégés)
# ══════════════════════════════════════════════════
@app.post("/payload/python", tags=["Payloads"])
def gen_python(req: PayloadRequest, _=Depends(require_auth)):
    if req.type != "python":
        raise HTTPException(400, "type doit être 'python'")
    try:
        from core.config import Config
        from modules.payload_generators.python_gen import PythonPayloadGenerator
        cfg = Config()
        cfg.set("lhost", req.lhost)
        cfg.set("lport", req.lport)
        result = PythonPayloadGenerator().run(cfg)
        webhook_manager.emit("payload.generated", {"type": "python", "lhost": req.lhost})
        return result
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/payload/cpp", tags=["Payloads"])
def gen_cpp(req: PayloadRequest, _=Depends(require_auth)):
    if req.type != "cpp":
        raise HTTPException(400, "type doit être 'cpp'")
    try:
        from core.config import Config
        from modules.payload_generators.cpp_gen import CppPayloadGenerator
        cfg = Config()
        cfg.set("lhost", req.lhost)
        cfg.set("lport", req.lport)
        result = CppPayloadGenerator().run(cfg)
        webhook_manager.emit("payload.generated", {"type": "cpp", "lhost": req.lhost})
        return result
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/payload/msfvenom", tags=["Payloads"])
def gen_msfvenom(req: PayloadRequest, _=Depends(require_auth)):
    if req.type != "msfvenom":
        raise HTTPException(400, "type doit être 'msfvenom'")
    try:
        from core.config import Config
        from modules.payload_generators.msfvenom_gen import MsfvenomGenerator
        cfg = Config()
        cfg.set("lhost", req.lhost)
        cfg.set("lport", req.lport)
        result = MsfvenomGenerator().run(cfg)
        webhook_manager.emit("payload.generated", {"type": "msfvenom", "lhost": req.lhost})
        return result
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/payloads", tags=["Payloads"])
def list_payloads(_=Depends(require_auth)):
    from core.database import Database
    return {"payloads": Database().get_all_payloads()}


# ══════════════════════════════════════════════════
#  RAPPORTS (protégés)
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
    content = MitreMapper().generate_report(req.actions)
    return {"report": content}


@app.get("/mitre/techniques", tags=["Reports"])
def mitre_techniques(_=Depends(require_auth)):
    from core.mitre import MitreMapper
    return {"techniques": MitreMapper().list_all()}


# ══════════════════════════════════════════════════
#  SCOPE (protégés)
# ══════════════════════════════════════════════════
@app.post("/scope/declare", tags=["Éthique"])
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


@app.get("/scope/active", tags=["Éthique"])
def get_active_scope(_=Depends(require_auth)):
    from core.scope import ScopeValidator
    scope = ScopeValidator().load_scope()
    return {"active": bool(scope), "scope": scope}


# ══════════════════════════════════════════════════
#  WEBHOOKS
# ══════════════════════════════════════════════════
@app.post("/webhooks/add", tags=["Webhooks"])
def add_webhook(req: WebhookRequest, _=Depends(require_auth)):
    webhook_manager.add_hook(req.url)
    return {"status": "success", "hooks": webhook_manager.hooks}


@app.get("/webhooks/list", tags=["Webhooks"])
def list_webhooks(_=Depends(require_auth)):
    return {"hooks": webhook_manager.hooks}


@app.post("/webhooks/test", tags=["Webhooks"])
def test_webhook(_=Depends(require_auth)):
    webhook_manager.emit("test", {"message": "FOKARAT test event"})
    return {"status": "queued"}


# ══════════════════════════════════════════════════
#  LANCEMENT
# ══════════════════════════════════════════════════
@app.on_event("startup")
def startup():
    webhook_manager.start()


@app.on_event("shutdown")
def shutdown():
    webhook_manager.stop()


def start_web(host="127.0.0.1", port=5000):
    """Démarre l'API (host par défaut : localhost uniquement pour la sécurité)."""
    import uvicorn
    uvicorn.run(app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    start_web()