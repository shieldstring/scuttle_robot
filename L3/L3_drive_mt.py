from L1.L1_motor import MotorController
from L2.L2_kinematics import Kinematics
from utils.constants import WHEELBASE
import logging
import time

logger = logging.getLogger(__name__)

class DriveController:
    def __init__(self):
        self.motor = MotorController()
        self.kinematics = Kinematics(WHEELBASE)
        self._running = False

        # safety variables 
        self._last_update = 0
        self._command_timeout = 0.5  # seconds
        
        logger.info("Drive controller initialized")

    def driving_thread(self):
        """Main control loop with safety checks"""
        self._running = True
        try:
            while self._running:
                 # Auto-stop if no recent commands
                if time.time() - self._last_update > self._command_timeout:
                    self.motor.stop()
                    time.sleep(0.1)
                    continue
                
                # Get commands from L2 systems
                x_dot, theta_dot = self._get_commands()  # Implement your logic
                
                # Convert to wheel speeds
                speeds = self.kinematics.compute_wheel_speeds(x_dot, theta_dot)
                         
                # Drive motors
                self.motor.set_speed(speeds)
                                
        except Exception as e:
            logger.error(f"Control error: {e}", exc_info=True)
            raise
        finally:
            self.motor.stop()
        
    def stop(self):
        self._running = False