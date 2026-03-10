# POST /api/explain
# Accepts a cassette image, returns Grad-CAM heatmap as base64.
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/explain")
async def explain():
    # TODO: call core.gradcam
    pass
