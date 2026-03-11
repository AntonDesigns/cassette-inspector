# Pydantic request and response models.
# Every endpoint input and output is typed here.
from pydantic import BaseModel
from typing import List, Optional

class PredictResponse(BaseModel):
    slots: List[int]
    confidence: List[float]
    inference_ms: int

class InspectRequest(BaseModel):
    image_b64: str
    machine_type: Optional[str] = None
    engineer: Optional[str] = None
