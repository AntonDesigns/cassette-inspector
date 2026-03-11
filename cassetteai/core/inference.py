import time
import base64
import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
import cv2
from pathlib import Path

# I handle model loading and prediction here and nothing else.
# I have no knowledge of the camera, the database, or the API.
#
# For v1 and v2 I use PyTorch with MobileNetV3. ONNX comes in at v3
# when the slot classifier moves into the YOLO ecosystem. If that switch
# happens, only this file needs to change. Nothing outside core/ will notice.
#
# I expect the model to output a probability distribution over the 7
# SlotOccupationState classes (0-6) for each of the 25 slots.
# I return the argmax as the predicted state and the max probability
# as the confidence score per slot.


class SlotInference:
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.last_inference_ms = None

        # I use the same transforms the model was trained with.
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])

    def load(self):
        # Load the PyTorch model onto whichever device is available.
        # I call this once on startup and again lazily if predict is
        # called before load.
        self.model = torch.load(str(self.model_path), map_location=self.device)
        self.model.eval()

    def is_loaded(self) -> bool:
        # The dashboard polls this via /api/status to show a model indicator.
        return self.model is not None

    def _decode_image(self, image):
        # Accept either a raw OpenCV frame or a base64 encoded string.
        # Routes can call predict either way without worrying about format.
        if isinstance(image, str):
            image_bytes = base64.b64decode(image)
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def predict(self, image) -> dict:
        if not self.is_loaded():
            self.load()

        rgb = self._decode_image(image)
        input_tensor = self.transform(rgb).unsqueeze(0).to(self.device)

        start = time.time()
        with torch.no_grad():
            output = self.model(input_tensor)
        elapsed_ms = int((time.time() - start) * 1000)

        self.last_inference_ms = elapsed_ms

        # output shape is (1, 25, 7): batch, slots, classes.
        # I take argmax across classes for the predicted state and
        # the softmax max as the confidence score.
        probabilities = torch.softmax(output[0], dim=-1).cpu().numpy()
        slots = [int(np.argmax(p)) for p in probabilities]
        confidence = [float(np.max(p)) for p in probabilities]

        return {
            "slots": slots,
            "confidence": confidence,
            "inference_ms": elapsed_ms,
        }
