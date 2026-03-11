import cv2

# I handle the camera in a separate class to keep the code organized and make it easier to swap
# If I ever swap OpenCV for a different camera library, only this file changes.
# source=0 is the laptop webcam. For a USB industrial camera I pass a different
# integer or a device path string.


class Camera:
    def __init__(self, source=0):
        self.source = source
        self.capture = None

    def open(self):
        # Open the video capture. I call this once on startup.
        self.capture = cv2.VideoCapture(self.source)

    def is_connected(self) -> bool:
        # The dashboard polls this via /api/status to show a camera indicator.
        return self.capture is not None and self.capture.isOpened()

    def capture_frame(self):
        # Grab a single frame and return it. If anything goes wrong I return
        # None so the caller can handle it gracefully instead of crashing.
        if not self.is_connected():
            self.open()

        if not self.is_connected():
            return None

        success, frame = self.capture.read()
        if not success:
            return None

        return frame

    def release(self):
        # Close the capture cleanly when the app shuts down.
        if self.capture is not None:
            self.capture.release()
            self.capture = None
