# Camera module — OpenCV only.
# Handles frame capture from webcam or industrial camera.
# Does not know about inference, the database, or the API.
import cv2

class Camera:
    def __init__(self, source=0):
        self.source = source
        self._cap = None

    def open(self):
        self._cap = cv2.VideoCapture(self.source)

    def capture_frame(self):
        if not self._cap:
            raise RuntimeError("Camera not open")
        ok, frame = self._cap.read()
        return frame if ok else None

    def release(self):
        if self._cap:
            self._cap.release()
