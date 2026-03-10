from fastapi import APIRouter
from api.schemas import InspectRequest, PredictResponse
from core.inference import SlotInference
from core.mapper import translate_neo_2000
from config import SLOT_MODEL_PATH

# Level 2 only. This endpoint is called by the Trymax NEO software
# via the PHP bridge on the NEO machine. It is not active in Level 1.
# To enable it, uncomment the include_router line in api/main.py.
#
# If machine_type is "2000" I run the raw values through the NEO 2000
# translation table before returning. If it is "uv" or missing I skip
# translation because the NEO UV already outputs SlotOccupationState directly.


router = APIRouter()
inference = SlotInference(SLOT_MODEL_PATH)


@router.post("/api/inspect", response_model=PredictResponse)
async def inspect(request: InspectRequest):
    result = inference.predict(request.image_b64)

    if request.machine_type == "2000":
        result["slots"] = translate_neo_2000(result["slots"])

    return PredictResponse(
        slots=result["slots"],
        confidence=result["confidence"],
        inference_ms=result["inference_ms"],
    )
