# Grad-CAM module — heatmap generation only.
# Does not know about the camera, the database, or the API.

class GradCAM:
    def __init__(self, model):
        self.model = model

    def generate(self, image):
        # Returns base64 heatmap overlay image
        # TODO: implement pytorch-grad-cam
        pass
