# Inference module — model loading and prediction only.
# Does not know about the camera, the database, or the API.
# Swap PyTorch for ONNX here without touching anything else.

class SlotInference:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None

    def load(self):
        # TODO: load PyTorch or ONNX model from self.model_path
        pass

    def predict(self, image):
        # Returns {"slots": [...], "confidence": [...], "inference_ms": int}
        # TODO: run inference
        pass
