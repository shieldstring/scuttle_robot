import pysicktim as lidar

class Lidar:
    def __init__(self):
        self.lidar = lidar.TiM561()

    def scan(self):
        # Get LIDAR scan data
        return self.lidar.scan()