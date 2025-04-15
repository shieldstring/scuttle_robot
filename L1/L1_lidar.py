import logging
from rplidar import RPLidar
from utils.logger import setup_logger

class Lidar:
    def __init__(self, port='/dev/ttyUSB0'):
        setup_logger()
        self.logger = logging.getLogger('lidar')
        self.port = port
        self.lidar = None
        self.connect()

    def connect(self):
        """Initialize connection to RPLIDAR"""
        try:
            self.lidar = RPLidar(self.port)
            self.logger.info(f"Connected to RPLIDAR on {self.port}")
        except Exception as e:
            self.logger.error(f"Connection failed: {str(e)}")
            raise

    def get_scan(self, max_scan_points=500):
        """Get one full 360° scan"""
        try:
            for scan in self.lidar.iter_scans(max_buf_meas=max_scan_points):
                return scan
        except Exception as e:
            self.logger.error(f"Scan error: {str(e)}")
            self.stop()
            raise

    def stop(self):
        """Clean shutdown"""
        if self.lidar:
            self.lidar.stop()
            self.lidar.disconnect()
            self.logger.info("RPLIDAR stopped")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()