from typing import List, Optional
from pydantic import BaseModel


# I keep every request and response model in this one file.

class PredictRequest(BaseModel):
    # The cassette image as a base64 string.
    # machine_type is "uv" or "2000". If None I assume uv and skip translation.
    image_b64: str
    machine_type: Optional[str] = None


class PredictResponse(BaseModel):
    # 25 SlotOccupationState integers, one per slot.
    # confidence is a float per slot between 0 and 1.
    # inference_ms tells the dashboard how long the model took.
    slots: List[int]
    confidence: List[float]
    inference_ms: int


class ExplainRequest(BaseModel):
    # Just the image. Grad-CAM does not need anything else.
    image_b64: str


class ExplainResponse(BaseModel):
    # The heatmap overlay returned as a base64 encoded image.
    # The dashboard renders it directly over the camera feed.
    heatmap_b64: str


class ConfirmRequest(BaseModel):
    # The engineer has reviewed the prediction and either accepted
    # it or corrected individual slots. I write the final result to
    # the database and flag the row in inspections.csv as reviewed.
    inspection_id: str
    slots: List[int]
    engineer: str


class StatusResponse(BaseModel):
    # Read only. The dashboard polls this on boot and periodically
    # to know whether the model and camera are ready.
    model_loaded: bool
    camera_connected: bool
    last_inference_ms: Optional[int] = None


# Level 2 only. 
# 
# The NEO software sends this via the PHP bridge.
# engineer is optional because the NEO software may not know who
# triggered the scan. If it is missing I leave reviewed_by blank.
class InspectRequest(BaseModel):
    image_b64: str
    machine_type: Optional[str] = None
    engineer: Optional[str] = None
