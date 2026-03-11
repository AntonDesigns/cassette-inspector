# POST /api/predict
# Accepts a cassette image, returns 25-slot predictions.
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/predict")
async def predict():
    # TODO: call core.inference
    pass
