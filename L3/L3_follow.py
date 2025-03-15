from L2.L2_track_target import TargetTracker
from L1.L1_camera import Camera

class FollowTarget:
    def __init__(self):
        self.camera = Camera()
        self.tracker = TargetTracker()

    def follow(self):
        while True:
            frame = self.camera.capture_frame()
            target_position = self.tracker.track_target(frame)
            # Add logic to follow the target