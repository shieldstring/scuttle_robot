import smbus2
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

class Encoder:
    def __init__(self, i2c_address):
        self.bus = smbus2.SMBus(1)
        self.address = i2c_address

    def read_position(self):
        """
        Read the encoder position from I2C.
        """
        try:
            data = self.bus.read_i2c_block_data(self.address, 0, 2)
            position = (data[0] << 8) | data[1]
            logging.debug(f"Encoder position: {position}")
            return position
        except Exception as e:
            logging.error(f"An error occurred while reading encoder position: {e}")
            raise