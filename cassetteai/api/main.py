from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.routes import predict, explain, snapshot, confirm, status

# This file does one thing: register routers and mount static files.

app = FastAPI(title="CassetteAI", version="1.0.0")

app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

templates = Jinja2Templates(directory="dashboard/templates")

app.include_router(predict.router)
app.include_router(explain.router)
app.include_router(snapshot.router)
app.include_router(confirm.router)
app.include_router(status.router)

# from api.routes import inspect
# app.include_router(inspect.router)


@app.get("/")
async def serve_dashboard(request):
    # Serve the dashboard. Everything else is handled by the routers.
    return templates.TemplateResponse("index.html", {"request": request})
