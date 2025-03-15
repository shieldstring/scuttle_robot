import numpy as np

class ObstacleDetector:
    def __init__(self):
        self.nearest_obstacle = None

    def detect_obstacle(self, lidar_data):
        # Find the nearest obstacle from LIDAR data
        distances = [point[0] for point in lidar_data]
        angles = [point[1] for point in lidar_data]
        min_distance = min(distances)
        min_index = distances.index(min_distance)
        self.nearest_obstacle = (min_distance, angles[min_index])
        return self.nearest_obstacle