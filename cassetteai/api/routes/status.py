from fastapi import APIRouter
from api.schemas import StatusResponse
from core.inference import SlotInference
from core.camera import Camera
from config import SLOT_MODEL_PATH

# This route is read only.

router = APIRouter()
inference = SlotInference(SLOT_MODEL_PATH)
camera = Camera(source=0)


@router.get("/api/status", response_model=StatusResponse)
async def status():
    return StatusResponse(
        model_loaded=inference.is_loaded(),
        camera_connected=camera.is_connected(),
        last_inference_ms=inference.last_inference_ms,
    )
