import smbus2

class Encoder:
    def __init__(self, i2c_address):
        self.bus = smbus2.SMBus(1)
        self.address = i2c_address

    def read_position(self):
        # Read encoder position from I2C
        data = self.bus.read_i2c_block_data(self.address, 0, 2)
        return (data[0] << 8) | data[1]