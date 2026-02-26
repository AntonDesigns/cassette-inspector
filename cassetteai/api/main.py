"""FastAPI application factory."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(
    title="CassetteAI",
    description="AI-powered semiconductor cassette inspection",
    version="0.1.0",
)

# Serve frontend static files
STATIC_DIR = Path(__file__).parent.parent / "frontend" / "static"
TEMPLATES_DIR = Path(__file__).parent.parent / "frontend" / "templates"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Routes will be registered here as they are built
# from cassetteai.api import predict, explain, snapshot, status, confirm
# app.include_router(predict.router)
# app.include_router(explain.router)
# app.include_router(snapshot.router)
# app.include_router(status.router)
# app.include_router(confirm.router)

@app.get("/api/status")
def status():
    return {"status": "ok", "version": "0.1.0"}
