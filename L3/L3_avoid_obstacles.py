import time
import numpy as np
from L2.L2_obstacle import ObstacleDetector
from L1.L1_lidar import Lidar
from utils.logger import setup_logger
import logging

class ObstacleAvoidance:
    def __init__(self, drive_system):
        """
        Enhanced obstacle avoidance system for SCUTTLE robot
        
        Args:
            drive_system: Initialized drive system from L3 layer
        """
        setup_logger()
        self.logger = logging.getLogger('avoidance')
        self.lidar = Lidar()
        self.obstacle_detector = ObstacleDetector(self.lidar)
        self.drive_system = drive_system
        
        # Configuration parameters
        self.safety_distance = 0.5  # meters
        self.escape_angle = 30      # degrees
        self.escape_speed = 0.3     # 0-1 (percentage of max speed)
        self.scan_sectors = 8       # For environment analysis

    def get_safest_direction(self, sector_distances):
        """
        Determine the safest escape direction based on sector distances
        
        Args:
            sector_distances: List of minimum distances per sector
            
        Returns:
            Tuple of (best_sector_index, sector_distance)
        """
        sector_angles = np.linspace(-180, 180, self.scan_sectors, endpoint=False)
        
        # Find all sectors with clearance
        safe_sectors = [(i, dist) for i, dist in enumerate(sector_distances) 
                       if dist > self.safety_distance]
        
        if not safe_sectors:
            return None  # No safe direction found
            
        # Prefer forward directions (sectors near 0°)
        def scoring_func(idx, dist):
            angle = abs(sector_angles[idx])
            return dist - (angle/180)  # Higher score for more forward directions
            
        # Select sector with highest score
        best_sector = max(safe_sectors, key=lambda x: scoring_func(x[0], x[1]))
        return sector_angles[best_sector[0]], best_sector[1]

    def execute_avoidance_maneuver(self, obstacle_direction):
        """
        Perform evasive action based on obstacle position
        
        Args:
            obstacle_direction: Angle to obstacle (degrees)
        """
        try:
            # Simple avoidance strategy - turn away from obstacle
            if obstacle_direction > 0:
                # Obstacle on right, turn left
                self.logger.info("Obstacle on right, turning left")
                self.drive_system.set_velocity(
                    linear=self.escape_speed * 0.5,
                    angular=self.escape_speed
                )
            else:
                # Obstacle on left, turn right
                self.logger.info("Obstacle on left, turning right")
                self.drive_system.set_velocity(
                    linear=self.escape_speed * 0.5,
                    angular=-self.escape_speed
                )
                
            time.sleep(1)  # Execute maneuver for 1 second
            self.drive_system.stop()
            
        except Exception as e:
            self.logger.error(f"Avoidance maneuver failed: {str(e)}")
            self.drive_system.emergency_stop()

    def avoid_obstacles(self):
        """Main obstacle avoidance loop"""
        self.logger.info("Starting obstacle avoidance system")
        
        try:
            while True:
                # Get environment data
                scan = self.lidar.get_scan()
                sector_distances = self.obstacle_detector.get_obstacle_map(scan, self.scan_sectors)
                
                # Check forward path
                if sector_distances[0] < self.safety_distance:
                    self.logger.warning(f"Obstacle detected at {sector_distances[0]:.2f}m")
                    
                    # Find safest escape direction
                    escape_info = self.get_safest_direction(sector_distances)
                    
                    if escape_info:
                        escape_angle, escape_dist = escape_info
                        self.logger.info(f"Escape direction found: {escape_angle:.0f}° ({escape_dist:.2f}m clear)")
                        self.execute_avoidance_maneuver(escape_angle)
                    else:
                        self.logger.warning("No clear path found - stopping")
                        self.drive_system.emergency_stop()
                        time.sleep(2)  # Wait before rechecking
                
                time.sleep(0.1)  # Main loop rate
                
        except KeyboardInterrupt:
            self.logger.info("Obstacle avoidance stopped by user")
        except Exception as e:
            self.logger.critical(f"Fatal error in avoidance: {str(e)}")
        finally:
            self.lidar.stop()
            self.drive_system.stop()

    def update_parameters(self, safety_dist=None, escape_angle=None, escape_speed=None):
        """Dynamically update avoidance parameters"""
        if safety_dist is not None and 0.1 <= safety_dist <= 2.0:
            self.safety_distance = safety_dist
        if escape_angle is not None and 10 <= escape_angle <= 90:
            self.escape_angle = escape_angle
        if escape_speed is not None and 0.1 <= escape_speed <= 0.8:
            self.escape_speed = escape_speed
            
        self.logger.info(
            f"Updated parameters: Safety={self.safety_distance}m, "
            f"Angle={self.escape_angle}°, Speed={self.escape_speed}"
        )