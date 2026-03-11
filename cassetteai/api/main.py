# CassetteAI - FastAPI entry point
# Registers all routers. No business logic lives here.
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="CassetteAI", version="1.0.0")

# TODO: import and register routers from api/routes/
