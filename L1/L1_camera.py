import cv2

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def capture_frame(self):
        ret, frame = self.cap.read()
        return frame