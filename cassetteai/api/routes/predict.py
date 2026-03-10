from fastapi import APIRouter
from api.schemas import PredictRequest, PredictResponse
from core.inference import SlotInference
from core.mapper import translate_neo_2000
from config import SLOT_MODEL_PATH

# This route does one thing: accept an image and return 25 slot predictions.
# If machine_type is "2000" I translate the raw mapper values before returning.

router = APIRouter()
inference = SlotInference(SLOT_MODEL_PATH)


@router.post("/api/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    result = inference.predict(request.image_b64)

    if request.machine_type == "2000":
        result["slots"] = translate_neo_2000(result["slots"])

    return PredictResponse(
        slots=result["slots"],
        confidence=result["confidence"],
        inference_ms=result["inference_ms"],
    )
