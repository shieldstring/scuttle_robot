import gpiozero
import logging
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Set the pin factory to pigpio (optional, for sharing GPIO pins between processes)
Device.pin_factory = PiGPIOFactory()

class MotorController:
    def __init__(self, pins):
        """
        Initialize the MotorController with a list of GPIO pins.
        Each pin should be unique to avoid conflicts.
        """
        # Ensure that no pin conflicts exist and that each pin is used once
        if len(set(pins)) != len(pins):
            raise ValueError("Pins must be unique. Duplicate pins found.")

        logging.debug(f"Initializing MotorController with pins: {pins}")

        try:
            # Initialize PWMOutputDevice for each motor
            self.motor_a = gpiozero.PWMOutputDevice(pins[0])
            self.motor_b = gpiozero.PWMOutputDevice(pins[1])
            self.motor_c = gpiozero.PWMOutputDevice(pins[2])
            self.motor_d = gpiozero.PWMOutputDevice(pins[3])

            logging.debug("MotorController initialized successfully.")
        except gpiozero.GPIOPinInUse as e:
            logging.error(f"GPIO pin conflict detected: {e}")
            raise
        except Exception as e:
            logging.error(f"An error occurred while initializing motors: {e}")
            raise

    def set_speed(self, duty_cycle):
        """
        Set the speed of all motors using a list of duty cycles.
        :param duty_cycle: List of duty cycles for each motor (e.g., [0.5, 0.5, 0.5, 0.5])
        """
        if len(duty_cycle) != 4:
            raise ValueError("Duty cycle list must contain exactly 4 values.")

        try:
            # Set the duty cycle for each motor
            self.motor_a.value = duty_cycle[0]
            self.motor_b.value = duty_cycle[1]
            self.motor_c.value = duty_cycle[2]
            self.motor_d.value = duty_cycle[3]

            logging.debug(f"Motor speeds set to: {duty_cycle}")
        except Exception as e:
            logging.error(f"An error occurred while setting motor speeds: {e}")
            raise