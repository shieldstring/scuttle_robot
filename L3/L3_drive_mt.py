import threading
from L1.L1_motor import MotorController
from L2.L2_kinematics import Kinematics
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

class DriveController:
    def __init__(self):
        self.motor_controller = MotorController([17, 18, 22, 23])
        self.kinematics = Kinematics(0.405)  # Wheelbase in meters

    def drive(self, x_dot, theta_dot):
        """
        Drive the robot based on desired x_dot and theta_dot.
        """
        try:
            phiL = x_dot - theta_dot * self.kinematics.wheelbase / 2
            phiR = x_dot + theta_dot * self.kinematics.wheelbase / 2
            self.motor_controller.set_speed([phiL, phiR, phiL, phiR])
            logging.debug(f"Driving with x_dot={x_dot}, theta_dot={theta_dot}")
        except Exception as e:
            logging.error(f"An error occurred while driving: {e}")
            raise

# Multithreading example
drive_controller = DriveController()

def driving_thread():
    while True:
        # Get x_dot and theta_dot from gamepad or autonomous logic
        x_dot, theta_dot = 0.5, 0.1  # Example values
        drive_controller.drive(x_dot, theta_dot)

thread = threading.Thread(target=driving_thread)
thread.start()