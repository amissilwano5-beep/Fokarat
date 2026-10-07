"""
FOKARAT - API REST Stable v1.0
Documentation : http://localhost:5000/docs
"""
import os
import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(
    title="FOKARAT API",
    version="1.0.0",
    description=(
        "API REST pour piloter FOKARAT. "
        "⚠️ Usage éducatif uniquement. Ne pas exposer sur Internet sans auth."
    ),
    contact={
        "name": "Lwano Amissi Blanchard (FOKAS)",
        "email": "amissilwano5@gmail.com",
    },
    license_info={"name": "MIT"},
)


# ══════════════════════════════════════════════════
#  MODÈLES
# ══════════════════════════════════════════════════
class PayloadRequest(BaseModel):
    type: str = Field(..., description="Type de payload : python, cpp, msfvenom")
    lhost: str = Field(..., description="Adresse IP d'écoute")
    lport: int = Field(..., ge=1, le=65535, description="Port d'écoute (1-65535)")


class ScopeRequest(BaseModel):
    target: str = Field(..., description="Cible autorisée")
    auth_ref: str = Field(..., description="Référence de l'autorisation écrite")
    hours: int = Field(24, ge=1, le=168, description="Durée en heures (max 168)")


class MitreRequest(BaseModel):
    actions: list = Field(..., description="Liste des actions (ex: ['padding','upx_pack'])")


# ══════════════════════════════════════════════════
#  ENDPOINTS
# ══════════════════════════════════════════════════
@app.get("/", tags=["Status"])
def root():
    """Retourne l'état général de l'API."""
    return {
        "framework": "FOKARAT",
        "version": "3.3.0",
        "api_version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/health", tags=["Status"])
def health():
    """Healthcheck simple."""
    return {"status": "ok"}


@app.get("/version", tags=["Status"])
def version():
    """Retourne les versions des composants."""
    return {
        "fokarat": "3.3.0",
        "api": "1.0.0",
        "python": sys.version.split()[0],
    }


# ─── PAYLOADS ─────────────────────────────────────
@app.post("/payload/python", tags=["Payloads"])
def gen_python(req: PayloadRequest):
    """Génère un payload Python."""
    if req.type != "python":
        raise HTTPException(status_code=400, detail="Type doit être 'python'")
    try:
        from core.config import Config
        from modules.payload_generators.python_gen import PythonPayloadGenerator
        cfg = Config()
        cfg.set("lhost", req.lhost)
        cfg.set("lport", req.lport)
        result = PythonPayloadGenerator().run(cfg)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/payload/cpp", tags=["Payloads"])
def gen_cpp(req: PayloadRequest):
    """Génère un payload C++."""
    if req.type != "cpp":
        raise HTTPException(status_code=400, detail="Type doit être 'cpp'")
    try:
        from core.config import Config
        from modules.payload_generators.cpp_gen import CppPayloadGenerator
        cfg = Config()
        cfg.set("lhost", req.lhost)
        cfg.set("lport", req.lport)
        return CppPayloadGenerator().run(cfg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/payload/msfvenom", tags=["Payloads"])
def gen_msfvenom(req: PayloadRequest):
    """Génère un payload MSFVenom."""
    if req.type != "msfvenom":
        raise HTTPException(status_code=400, detail="Type doit être 'msfvenom'")
    try:
        from core.config import Config
        from modules.payload_generators.msfvenom_gen import MsfvenomGenerator
        cfg = Config()
        cfg.set("lhost", req.lhost)
        cfg.set("lport", req.lport)
        return MsfvenomGenerator().run(cfg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/payloads", tags=["Payloads"])
def list_payloads():
    """Liste tous les payloads générés."""
    try:
        from core.database import Database
        return {"payloads": Database().get_all_payloads()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── SESSIONS ─────────────────────────────────────
@app.get("/listeners", tags=["Listeners"])
def list_listeners():
    """Liste tous les listeners enregistrés."""
    try:
        from core.database import Database
        return {"listeners": Database().get_all_listeners()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── RAPPORTS ─────────────────────────────────────
@app.get("/report", tags=["Reports"])
def report():
    """Génère et retourne un rapport d'opérations."""
    try:
        from core.database import Database
        path = Database().export_report()
        with open(path, "r", encoding="utf-8") as f:
            return {"report": f.read(), "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/report/mitre", tags=["Reports"])
def report_mitre(req: MitreRequest):
    """Génère un rapport MITRE ATT&CK à partir d'une liste d'actions."""
    try:
        from core.mitre import MitreMapper
        mapper = MitreMapper()
        content = mapper.generate_report(req.actions)
        return {"report": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mitre/techniques", tags=["Reports"])
def mitre_techniques():
    """Liste toutes les techniques MITRE connues."""
    from core.mitre import MitreMapper
    return {"techniques": MitreMapper().list_all()}


# ─── SCOPE ────────────────────────────────────────
@app.post("/scope/declare", tags=["Éthique"])
def declare_scope(req: ScopeRequest):
    """Déclare un scope autorisé (obligatoire avant toute attaque)."""
    try:
        from core.scope import ScopeValidator
        sv = ScopeValidator()
        # Utilise la méthode _ask_confirmation en mode silencieux
        import datetime
        scope = {
            "target": req.target,
            "auth_ref": req.auth_ref,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "expires_at": (datetime.datetime.utcnow() +
                          datetime.timedelta(hours=req.hours)).isoformat(),
            "hours": req.hours,
        }
        import json
        os.makedirs("output", exist_ok=True)
        with open(sv.SCOPE_FILE, "w") as f:
            json.dump(scope, f, indent=2)
        return {"status": "success", "scope": scope}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scope/active", tags=["Éthique"])
def get_active_scope():
    """Retourne le scope actif s'il existe."""
    from core.scope import ScopeValidator
    scope = ScopeValidator().load_scope()
    if not scope:
        return {"active": False, "scope": None}
    return {"active": True, "scope": scope}


# ══════════════════════════════════════════════════
#  LANCEMENT
# ══════════════════════════════════════════════════
def start_web(host="0.0.0.0", port=5000):
    import uvicorn
    uvicorn.run(app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    start_web()