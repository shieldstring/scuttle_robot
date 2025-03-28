from L3.L3_drive_mt import DriveController
from L3.L3_avoid_obstacles import ObstacleAvoidance
from L3.L3_follow import FollowTarget
from L1.L1_gamepad import Gamepad
import threading
import time
import logging

logger = logging.getLogger(__name__)

class MissionControl:
    def __init__(self):
        self.drive_controller = DriveController()
        self.obstacle_avoidance = ObstacleAvoidance(self.drive_controller)
        self.follow_target = FollowTarget(self.drive_controller)
        self.gamepad = Gamepad()
        self._running = False
        self._threads = []
        self._control_mode = "AUTO"  # or "MANUAL"

    def start_mission(self):
        """Start all systems with gamepad monitoring"""
        if self._running:
            logger.warning("Mission already running")
            return

        self._running = True
        
        # Start core threads
        components = [
            (self._drive_thread, "DriveSystem"),
            (self._gamepad_thread, "GamepadMonitor"),
            (self._mode_manager, "ModeManager")
        ]

        try:
            for target, name in components:
                thread = threading.Thread(
                    target=target,
                    name=name,
                    daemon=True
                )
                self._threads.append(thread)
                thread.start()
                logger.info(f"Started {name} thread")

            while self._running:
                if not any(t.is_alive() for t in self._threads):
                    logger.error("Critical threads stopped!")
                    break
                time.sleep(0.5)

        except Exception as e:
            logger.critical(f"Mission failed: {e}")
            self.stop_mission()

    def _drive_thread(self):
        """Handle driving based on current mode"""
        while self._running:
            if self._control_mode == "AUTO":
                # Autonomous operation
                self.obstacle_avoidance.avoid_obstacles()
                self.follow_target.follow()
            time.sleep(0.05)

    def _gamepad_thread(self):
        """Continuous gamepad monitoring"""
        while self._running:
            try:
                x, y = self.gamepad.get_input()
                
                # Mode toggle using gamepad button (example: Triangle button)
                if self.gamepad.joystick.get_button(2):  # Button index may vary
                    self._toggle_mode()
                
                if self._control_mode == "MANUAL":
                    self._handle_manual_control(x, y)
                    
                time.sleep(0.02)
                
            except Exception as e:
                logger.error(f"Gamepad error: {e}")
                time.sleep(1)

    def _toggle_mode(self):
        """Switch between AUTO and MANUAL modes"""
        self._control_mode = "MANUAL" if self._control_mode == "AUTO" else "AUTO"
        logger.info(f"Control mode changed to {self._control_mode}")
        
        # Reset systems when switching modes
        if self._control_mode == "AUTO":
            self.drive_controller.stop()

    def _handle_manual_control(self, x, y):
        """Convert gamepad input to drive commands"""
        # Convert joystick to robot commands
        forward_speed = y * 0.5  # Scale as needed
        turn_speed = x * 0.3     # Scale as needed
        
        # Send to drive controller
        self.drive_controller.set_speed((forward_speed + turn_speed, 
                                       forward_speed - turn_speed))

    def stop_mission(self):
        """Graceful shutdown"""
        self._running = False
        self.drive_controller.stop()
        
        for t in self._threads:
            if t.is_alive():
                t.join(timeout=1)