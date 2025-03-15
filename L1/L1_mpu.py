import smbus2

class MPU9250:
    def __init__(self, i2c_address=0x68):
        self.bus = smbus2.SMBus(1)
        self.address = i2c_address

    def read_data(self):
        # Read accelerometer, gyroscope, and magnetometer data
        accel_data = self.bus.read_i2c_block_data(self.address, 0x3B, 6)
        gyro_data = self.bus.read_i2c_block_data(self.address, 0x43, 6)
        mag_data = self.bus.read_i2c_block_data(self.address, 0x03, 6)
        return accel_data, gyro_data, mag_data