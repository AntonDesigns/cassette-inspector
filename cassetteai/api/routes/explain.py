from fastapi import APIRouter
from api.schemas import ExplainRequest, ExplainResponse
from core.gradcam import GradCAM
from config import SLOT_MODEL_PATH

# This route does one thing: accept an image and return a Grad-CAM heatmap.

router = APIRouter()
gradcam = GradCAM(SLOT_MODEL_PATH)


@router.post("/api/explain", response_model=ExplainResponse)
async def explain(request: ExplainRequest):
    heatmap_b64 = gradcam.generate(request.image_b64)

    return ExplainResponse(heatmap_b64=heatmap_b64)
