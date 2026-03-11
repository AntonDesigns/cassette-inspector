# POST /api/snapshot
# Captures current camera frame, runs prediction, writes to DB.
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/snapshot")
async def snapshot():
    # TODO: call core.camera + core.inference + db
    pass
