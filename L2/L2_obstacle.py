import logging
from utils.logger import setup_logger

class ObstacleDetector:
    def __init__(self, lidar):
        setup_logger()
        self.logger = logging.getLogger('obstacle')
        self.lidar = lidar

    def get_front_obstacles(self, scan, cone_angle=45):
        """Return obstacles in front cone"""
        if not scan:
            return None
        return [p for p in scan if -cone_angle <= p[1] <= cone_angle]

    def get_min_distance(self, scan):
        """Get minimum distance in meters"""
        front_scan = self.get_front_obstacles(scan)
        if front_scan:
            return min(p[2] for p in front_scan) / 1000.0  # mm to m
        return float('inf')