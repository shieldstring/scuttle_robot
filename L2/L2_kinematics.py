import numpy as np

class Kinematics:
    def __init__(self, wheelbase):
        self.wheelbase = wheelbase

    def compute_chassis_movement(self, phiL, phiR):
        # Compute chassis movement based on wheel speeds
        x_dot = (phiL + phiR) / 2
        theta_dot = (phiR - phiL) / self.wheelbase
        return x_dot, theta_dot