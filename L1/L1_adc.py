import smbus2

class ADC:
    def __init__(self, i2c_address=0x48):
        self.bus = smbus2.SMBus(1)
        self.address = i2c_address

    def read_voltage(self):
        # Read voltage from ADC
        data = self.bus.read_i2c_block_data(self.address, 0, 2)
        return (data[0] << 8) | data[1]