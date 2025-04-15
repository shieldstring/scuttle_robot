from L1.L1_motor import MotorController
from L2.L2_kinematics import Kinematics
from utils.constants import WHEELBASE
import logging
import time
import threading
from typing import Tuple

logger = logging.getLogger(__name__)

class DriveController:
    def __init__(self):
        self.motor = MotorController()
        self.kinematics = Kinematics(WHEELBASE)
        self._running = False
        self._last_update = 0
        self._command_timeout = 0.5  # seconds
        self._lock = threading.Lock()
        self._current_velocity = (0.0, 0.0)  # (linear, angular)
        logger.info("Drive controller initialized")

    def driving_thread(self):
        """Main control loop with safety checks"""
        self._running = True
        try:
            while self._running:
                # Safety timeout check
                if time.time() - self._last_update > self._command_timeout:
                    self._emergency_stop()
                    time.sleep(0.1)
                    continue
                
                # Get current velocity command
                with self._lock:
                    linear, angular = self._current_velocity
                
                # Compute and execute wheel speeds
                speeds = self.kinematics.compute_wheel_speeds(linear, angular)
                self.motor.set_speed(speeds)
                
                time.sleep(0.02)  # 50Hz control loop
                                
        except Exception as e:
            logger.error(f"Control error: {e}", exc_info=True)
            self._emergency_stop()
            raise
        finally:
            self._emergency_stop()
        
    def set_velocity(self, linear: float, angular: float):
        """Thread-safe velocity command"""
        with self._lock:
            self._current_velocity = (linear, angular)
            self._last_update = time.time()

    def stop(self):
        """Normal stop procedure"""
        with self._lock:
            self._current_velocity = (0.0, 0.0)
            self._last_update = time.time()

    def emergency_stop(self):
        """Immediate halt"""
        self._emergency_stop()

    def _emergency_stop(self):
        """Internal emergency stop"""
        with self._lock:
            self._current_velocity = (0.0, 0.0)
            self.motor.stop(emergency=True)


class DriveSystem:
    def __init__(self):
        self.controller = DriveController()
        self.control_thread = threading.Thread(
            target=self.controller.driving_thread,
            daemon=True
        )
        logger.info("Drive system initialized")

    def start(self):
        """Start the drive system thread"""
        self.control_thread.start()
        logger.info("Drive system started")

    def set_velocity(self, linear: float, angular: float):
        """Set desired velocity (thread-safe)"""
        self.controller.set_velocity(linear, angular)

    def stop(self):
        """Graceful stop"""
        self.controller.stop()

    def emergency_stop(self):
        """Immediate emergency stop"""
        self.controller.emergency_stop()