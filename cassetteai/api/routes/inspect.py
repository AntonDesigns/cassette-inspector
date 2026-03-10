# POST /api/inspect  (Level 2)
# Called by Trymax NEO software via the PHP bridge.
# Accepts a cassette image, returns SlotOccupationState[] JSON.
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/inspect")
async def inspect():
    # TODO: call core.inference + core.mapper
    pass
