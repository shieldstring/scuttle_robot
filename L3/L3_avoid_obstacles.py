from L2.L2_obstacle import ObstacleDetector
from L1.L1_lidar import Lidar

class ObstacleAvoidance:
    def __init__(self):
        self.lidar = Lidar()
        self.obstacle_detector = ObstacleDetector()

    def avoid_obstacles(self):
        while True:
            lidar_data = self.lidar.scan()
            nearest_obstacle = self.obstacle_detector.detect_obstacle(lidar_data)
            if nearest_obstacle[0] < 0.5:  # If obstacle is within 0.5 meters
                print("Obstacle detected! Taking evasive action.")
                # Add logic to avoid the obstacle