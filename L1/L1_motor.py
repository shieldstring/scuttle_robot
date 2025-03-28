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
        self._is_emergency_stopped = False

    def set_speed(self, speeds):
        """Set speeds between -1.0 (full reverse) and 1.0 (full forward)"""
        for motor, speed in zip(self.motors, speeds):
            motor.value = max(-1.0, min(1.0, speed))
        logger.debug(f"Motor speeds set: {speeds}")

    def stop(self, emergency=False):
        
        """Stop all motors
        Args:
            emergency: If True, logs as warning (for unexpected stops)
        """
        self._is_emergency_stopped = emergency

        for motor in self.motors:
            motor.value = 0
        if emergency:
            logger.warning("Motors forcefully stopped")
        else:
            logger.info("Motors stopped normally")
            
    def status(self):
        return {
            "emergency_stop": self._is_emergency_stopped,
            "speeds": [m.value for m in self.motors]
        }