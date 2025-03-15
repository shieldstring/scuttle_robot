from L3.L3_drive_mt import DriveController
from L3.L3_avoid_obstacles import ObstacleAvoidance
from L3.L3_follow import FollowTarget
import threading

class MissionControl:
    def __init__(self):
        self.drive_controller = DriveController()
        self.obstacle_avoidance = ObstacleAvoidance()
        self.follow_target = FollowTarget()

    def start_mission(self):
        # Start threads for driving, obstacle avoidance, and target following
        drive_thread = threading.Thread(target=self.drive_controller.driving_thread)
        obstacle_thread = threading.Thread(target=self.obstacle_avoidance.avoid_obstacles)
        follow_thread = threading.Thread(target=self.follow_target.follow)

        drive_thread.start()
        obstacle_thread.start()
        follow_thread.start()

        drive_thread.join()
        obstacle_thread.join()
        follow_thread.join()