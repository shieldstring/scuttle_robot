import time
from L3.L3_drive_mt import DriveSystem
from L3.L3_mission_control import MissionControl
from utils.logger import setup_logger
import signal
import logging

# Initialize the logger (no arguments needed as per your setup)
setup_logger()
logger = logging.getLogger('main')  # Create named logger after setup

def shutdown_handler(signum, frame):
    logger.warning("Shutdown signal received")
    if 'drive_system' in globals():
        drive_system.stop()
    exit(0)

def signal_handler(sig, frame):
    logging.warning("Shutting down...")
    if 'mission' in globals():
        MissionControl.stop_mission()
    exit(0)

if __name__ == "__main__":
    # Register shutdown handlers
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        logger.info("Starting SCUTTLE robot")
        drive_system = DriveSystem()
        drive_system.start()
        
        # Main blocking loop
        while True:
            time.sleep(1)
            
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        if 'drive_system' in locals():
            drive_system.stop()