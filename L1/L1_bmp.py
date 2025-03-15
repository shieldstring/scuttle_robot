import smbus2

class BMP280:
    def __init__(self, i2c_address=0x76):
        self.bus = smbus2.SMBus(1)
        self.address = i2c_address

    def read_data(self):
        # Read temperature and pressure data
        temp_data = self.bus.read_i2c_block_data(self.address, 0xFA, 3)
        press_data = self.bus.read_i2c_block_data(self.address, 0xF7, 3)
        return temp_data, press_data