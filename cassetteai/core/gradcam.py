import base64
import numpy as np
import cv2
from pathlib import Path

# I handle Grad-CAM heatmap generation here and nothing else.
# I have no knowledge of the camera, the database, or the API.
#
# I use the pytorch-grad-cam library which works with most CNN architectures.
# The heatmap shows the engineer which parts of the image the model focused
# on when making its prediction. I return it as a base64 string so the
# dashboard can render it directly as an image overlay.
#
# Note: Grad-CAM requires a PyTorch model, not ONNX. I load the model
# separately here using PyTorch for explanation only. The main inference
# still runs through ONNX in inference.py. This is intentional. Explanation
# is a separate concern from prediction.


class GradCAM:
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self.model = None
        self.cam = None

    def _load(self):
        import torch
        from pytorch_grad_cam import GradCAM as GradCAMLib
        from pytorch_grad_cam.utils.image import show_cam_on_image

        self.torch = torch
        self.show_cam_on_image = show_cam_on_image

        # I load the PyTorch model for explanation only.
        # The target layer is the last convolutional layer, which gives
        # the most meaningful spatial heatmap for slot detection.
        self.model = torch.load(str(self.model_path), map_location="cpu")
        self.model.eval()

        target_layer = list(
            filter(lambda m: isinstance(m, torch.nn.Conv2d), self.model.modules())
        )[-1]

        self.cam = GradCAMLib(model=self.model, target_layers=[target_layer])

    def generate(self, image) -> str:
        # Accept either a raw OpenCV frame or a base64 encoded string.
        if isinstance(image, str):
            image_bytes = base64.b64decode(image)
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if self.cam is None:
            self._load()

        # Resize and normalize the image for the model.
        resized = cv2.resize(image, (224, 224))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        float_image = np.float32(rgb) / 255.0

        input_tensor = self.torch.tensor(float_image).permute(2, 0, 1).unsqueeze(0)

        grayscale_cam = self.cam(input_tensor=input_tensor)[0]

        # Overlay the heatmap on the original image.
        heatmap = self.show_cam_on_image(float_image, grayscale_cam, use_rgb=True)
        heatmap_bgr = cv2.cvtColor(heatmap, cv2.COLOR_RGB2BGR)

        # Encode to base64 so the dashboard can use it as an img src directly.
        _, buffer = cv2.imencode(".jpg", heatmap_bgr)
        heatmap_b64 = base64.b64encode(buffer).decode("utf-8")

        return heatmap_b64
