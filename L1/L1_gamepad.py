import pygame
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

class Gamepad:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def get_input(self):
        """
        Get input from the gamepad.
        """
        try:
            pygame.event.pump()
            x_axis = self.joystick.get_axis(0)  # Left stick X-axis
            y_axis = self.joystick.get_axis(1)  # Left stick Y-axis
            logging.debug(f"Gamepad input: x_axis={x_axis}, y_axis={y_axis}")
            return x_axis, y_axis
        except Exception as e:
            logging.error(f"An error occurred while reading gamepad input: {e}")
            raise