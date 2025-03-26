from utils.constants import WHEELBASE
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Kinematics:
    def __init__(self, wheelbase=WHEELBASE):
        """Initialize with wheelbase from constants.py"""
        self.wheelbase = wheelbase
        logger.info(f"Kinematics initialized with wheelbase: {self.wheelbase}m")

    def compute_chassis_speeds(self, phi_l, phi_r):
        """
        Convert wheel speeds to chassis movement
        phi_l, phi_r: left/right wheel speeds in rad/s
        Returns: (x_dot, theta_dot) in m/s and rad/s
        """
        x_dot = (phi_l + phi_r) / 2
        theta_dot = (phi_r - phi_l) / self.wheelbase
        logger.debug(f"Computed chassis speeds: x_dot={x_dot:.2f}m/s, theta_dot={theta_dot:.2f}rad/s")
        return x_dot, theta_dot

    def compute_wheel_speeds(self, x_dot, theta_dot):
        """
        Convert chassis commands to wheel speeds
        x_dot: desired forward speed (m/s)
        theta_dot: desired angular speed (rad/s)
        Returns: [left_speed, right_speed] in rad/s
        """
        phi_l = x_dot - (theta_dot * self.wheelbase) / 2
        phi_r = x_dot + (theta_dot * self.wheelbase) / 2
        logger.debug(f"Computed wheel speeds: left={phi_l:.2f}rad/s, right={phi_r:.2f}rad/s")
        return [phi_l, phi_r]

    def compute_motor_commands(self, x_dot, theta_dot):
        """
        Directly compute motor duty cycles (-1 to 1)
        Returns: [left_duty, right_duty, left_duty, right_duty]
        """
        phi_l, phi_r = self.compute_wheel_speeds(x_dot, theta_dot)
        # Scale to motor duty cycles (assuming MAX_SPEED from constants)
        from utils.constants import MAX_SPEED
        left_duty = phi_l / MAX_SPEED
        right_duty = phi_r / MAX_SPEED
        return [left_duty, right_duty, left_duty, right_duty]