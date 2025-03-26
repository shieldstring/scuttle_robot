import time
from L3.L3_drive_mt import DriveSystem
from utils.logger import setup_logger
import signal

logger = setup_logger('main')

def shutdown_handler(signum, frame):
    logger.warning("Shutdown signal received")
    drive_system.stop()
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
        drive_system.stop()