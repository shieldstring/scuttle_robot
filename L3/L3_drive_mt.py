from L1.L1_motor import MotorController
from L2.L2_kinematics import Kinematics
from utils.constants import WHEELBASE
import logging
import time
import threading

logger = logging.getLogger(__name__)

class DriveController:
    def __init__(self):
        self.motor = MotorController()
        self.kinematics = Kinematics(WHEELBASE)
        self._running = False
        self._last_update = 0
        self._command_timeout = 0.5  # seconds
        logger.info("Drive controller initialized")

    def driving_thread(self):
        """Main control loop with safety checks"""
        self._running = True
        try:
            while self._running:
                if time.time() - self._last_update > self._command_timeout:
                    self.motor.stop()
                    time.sleep(0.1)
                    continue
                
                x_dot, theta_dot = self._get_commands()  # Implement your logic
                speeds = self.kinematics.compute_wheel_speeds(x_dot, theta_dot)
                self.motor.set_speed(speeds)
                                
        except Exception as e:
            logger.error(f"Control error: {e}", exc_info=True)
            raise
        finally:
            self.motor.stop()
        
    def stop(self):
        self._running = False

    def _get_commands(self):
        """Placeholder for command input"""
        return 0.0, 0.0  # Implement your command logic here


class DriveSystem:
    def __init__(self):
        self.controller = DriveController()
        self.control_thread = threading.Thread(target=self.controller.driving_thread)
        logger.info("Drive system initialized")

    def start(self):
        """Start the drive system thread"""
        self.control_thread.start()
        logger.info("Drive system started")

    def stop(self):
        """Stop the drive system"""
        self.controller.stop()
        self.control_thread.join()
        logger.info("Drive system stopped")