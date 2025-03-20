import numpy as np
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

class Kinematics:
    def __init__(self, wheelbase):
        self.wheelbase = wheelbase

    def compute_chassis_movement(self, phiL, phiR):
        """
        Compute chassis movement based on wheel speeds.
        """
        try:
            x_dot = (phiL + phiR) / 2
            theta_dot = (phiR - phiL) / self.wheelbase
            logging.debug(f"Chassis movement: x_dot={x_dot}, theta_dot={theta_dot}")
            return x_dot, theta_dot
        except Exception as e:
            logging.error(f"An error occurred while computing chassis movement: {e}")
            raise