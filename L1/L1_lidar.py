import pysicktim as lidar
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

class Lidar:
    def __init__(self):
        self.lidar = lidar.TiM561()

    def scan(self):
        """
        Get LIDAR scan data.
        """
        try:
            scan_data = self.lidar.scan()
            logging.debug(f"LIDAR scan data: {scan_data}")
            return scan_data
        except Exception as e:
            logging.error(f"An error occurred while scanning with LIDAR: {e}")
            raise