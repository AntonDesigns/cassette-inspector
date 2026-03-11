# GET /api/status
# Returns model status, last inference time, camera connection state.
from fastapi import APIRouter
router = APIRouter()

@router.get("/api/status")
async def status():
    # TODO: return live status from core modules
    pass
