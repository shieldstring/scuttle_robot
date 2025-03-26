import gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory
from utils.constants import MOTOR_PINS, PWM_FREQUENCY
import logging

logger = logging.getLogger(__name__)

class MotorController:
    def __init__(self):
        """Initialize with pigpio for hardware PWM"""
        gpiozero.Device.pin_factory = PiGPIOFactory()
        self.motors = [
            gpiozero.PWMOutputDevice(
                pin=pin,
                frequency=PWM_FREQUENCY,
                initial_value=0
            ) for pin in MOTOR_PINS
        ]
        logger.info(f"Motors ready on pins: {MOTOR_PINS}")

    def set_speed(self, speeds):
        """Set speeds between -1.0 (full reverse) and 1.0 (full forward)"""
        for motor, speed in zip(self.motors, speeds):
            motor.value = max(-1.0, min(1.0, speed))
        logger.debug(f"Motor speeds set: {speeds}")

    def stop(self):
        """Emergency stop all motors"""
        for motor in self.motors:
            motor.value = 0
        logger.warning("Motors forcefully stopped")