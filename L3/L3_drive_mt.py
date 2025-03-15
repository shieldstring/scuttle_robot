import threading
from L1.L1_motor import MotorController
from L2.L2_kinematics import Kinematics

class DriveController:
    def __init__(self):
        self.motor_controller = MotorController([11, 12, 15, 16])
        self.kinematics = Kinematics(0.405)  # Wheelbase in meters

    def drive(self, x_dot, theta_dot):
        # Compute wheel speeds and set motor duty cycles
        phiL = x_dot - theta_dot * self.kinematics.wheelbase / 2
        phiR = x_dot + theta_dot * self.kinematics.wheelbase / 2
        self.motor_controller.set_speed([phiL, phiR, phiL, phiR])

# Multithreading example
drive_controller = DriveController()

def driving_thread():
    while True:
        # Get x_dot and theta_dot from gamepad or autonomous logic
        x_dot, theta_dot = 0.5, 0.1  # Example values
        drive_controller.drive(x_dot, theta_dot)

thread = threading.Thread(target=driving_thread)
thread.start()