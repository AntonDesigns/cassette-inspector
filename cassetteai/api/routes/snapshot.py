import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from api.schemas import PredictResponse
from core.camera import Camera
from core.inference import SlotInference
from db.base import get_db
from config import SLOT_MODEL_PATH

# This is the only route that touches all three core modules.
# Camera captures the frame, inference predicts the slots, then
# I write the result to the database so the dashboard history works.
# I also write to inspections.csv so the result enters the training pipeline.

router = APIRouter()
camera = Camera(source=0)
inference = SlotInference(SLOT_MODEL_PATH)


@router.post("/api/snapshot", response_model=PredictResponse)
async def snapshot():
    frame = camera.capture_frame()

    if frame is None:
        raise HTTPException(status_code=503, detail="Camera is not available.")

    result = inference.predict(frame)

    inspection_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    db = get_db()
    db.write_inspection({
        "inspection_id": inspection_id,
        "timestamp_utc": timestamp,
        "slots": result["slots"],
        "confidence": result["confidence"],
        "inference_ms": result["inference_ms"],
        "final_status": "pending",
        "needs_review": False,
    })

    return PredictResponse(
        slots=result["slots"],
        confidence=result["confidence"],
        inference_ms=result["inference_ms"],
    )
