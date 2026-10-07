"""
FOKARAT - API REST (FastAPI)
Pilotage du framework via HTTP.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="FOKARAT API", version="2.0")


class PayloadRequest(BaseModel):
    type: str
    lhost: str
    lport: int


@app.get("/")
def root():
    return {"framework": "FOKARAT", "version": "2.0", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/payload/python")
def gen_python(req: PayloadRequest):
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


@app.get("/payloads")
def list_payloads():
    from core.database import Database
    return {"payloads": Database().get_all_payloads()}


@app.get("/report")
def report():
    from core.database import Database
    path = Database().export_report()
    return {"report": path}


def start_web(host="0.0.0.0", port=5000):
    import uvicorn
    uvicorn.run(app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    start_web()