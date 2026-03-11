import time
import base64
import numpy as np
import onnxruntime as ort
import cv2
from pathlib import Path

# I handle model loading and prediction here 
# I use ONNX for deployment because it removes the PyTorch dependency
# at runtime. If the model format ever needs to change, only this file
# changes.
# I expect the model to output a probability distribution over the 7 SlotOccupationState classes (0-6) for each of the 25 slots.
# I return the argmax as the predicted state and the max probability as the confidence score.


class SlotInference:
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self.session = None
        self.last_inference_ms = None

    def load(self):
        # Load the ONNX model. I call this once on startup.
        self.session = ort.InferenceSession(str(self.model_path))

    def is_loaded(self) -> bool:
        # The dashboard polls this via /api/status to show a model indicator.
        return self.session is not None

    def _preprocess(self, image) -> np.ndarray:
        # Resize to the input size the model was trained on, normalize,
        # and add the batch dimension ONNX expects.
        image = cv2.resize(image, (224, 224))
        image = image.astype(np.float32) / 255.0
        image = np.transpose(image, (2, 0, 1))
        image = np.expand_dims(image, axis=0)
        return image

    def predict(self, image) -> dict:
        # Accept either a raw OpenCV frame or a base64 encoded string.
        # Routes can call this either way without worrying about format.
        if isinstance(image, str):
            image_bytes = base64.b64decode(image)
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if not self.is_loaded():
            self.load()

        input_tensor = self._preprocess(image)
        input_name = self.session.get_inputs()[0].name

        start = time.time()
        outputs = self.session.run(None, {input_name: input_tensor})
        elapsed_ms = int((time.time() - start) * 1000)

        self.last_inference_ms = elapsed_ms

        # outputs[0] shape is (1, 25, 7): batch, slots, classes
        probabilities = outputs[0][0]
        slots = [int(np.argmax(p)) for p in probabilities]
        confidence = [float(np.max(p)) for p in probabilities]

        return {
            "slots": slots,
            "confidence": confidence,
            "inference_ms": elapsed_ms,
        }
