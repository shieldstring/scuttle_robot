import time
import signal
import logging
from L3.L3_drive_mt import DriveSystem
from L3.L3_mission_control import MissionControl
from L1.L1_lidar import Lidar
from L2.L2_obstacle import ObstacleDetector
from utils.logger import setup_logger

def shutdown_handler(signum, frame):
    logging.warning("Shutdown signal received")
    if 'mission' in globals():
        mission.stop_mission()
    exit(0)

if __name__ == "__main__":
    # Initialize systems
    setup_logger()
    logger = logging.getLogger('main')
    
    # Register shutdown handlers
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    
    try:
        logger.info("Starting SCUTTLE robot systems")
        
        # Hardware layer
        with Lidar() as lidar:
            # Logic layer
            obstacle_detector = ObstacleDetector(lidar)
            
            # Mission control layer
            drive_system = DriveSystem()
            mission = MissionControl(drive_system)
            
            # Start systems
            drive_system.start()
            mission.start_mission()
            
            # Main monitoring loop
            while True:
                scan = lidar.get_scan()
                if scan:
                    min_dist = obstacle_detector.get_min_distance(scan)
                    if min_dist < 0.5:  # Safety threshold
                        logger.warning(f"Obstacle detected at {min_dist:.2f}m")
                        mission._trigger_safety_hold()
                
                time.sleep(0.1)  # Monitoring rate
                
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        if 'mission' in locals():
            mission.stop_mission()
        exit(1)