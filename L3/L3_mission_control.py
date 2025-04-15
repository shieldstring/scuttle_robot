from L3.L3_drive_mt import DriveSystem
from L3.L3_avoid_obstacles import ObstacleAvoidance
from L3.L3_follow import FollowTarget
from L1.L1_gamepad import Gamepad
import threading
import time
import logging
from enum import Enum, auto
from typing import Optional, Dict, Tuple

logger = logging.getLogger(__name__)

class ControlMode(Enum):
    """Operation mode enumeration"""
    MANUAL = auto()
    AUTO = auto()
    SAFETY_HOLD = auto()

class MissionControl:
    def __init__(self):
        """Initialize mission control system with integrated obstacle avoidance"""
        # Initialize core systems
        self.drive_system = DriveSystem()
        self.obstacle_avoidance = ObstacleAvoidance(self.drive_system)
        self.follow_target = FollowTarget(self.drive_system)
        self.gamepad = Gamepad()
        
        # Configure avoidance parameters
        self.obstacle_avoidance.update_parameters(
            safety_dist=0.6,  # Larger safety margin
            escape_speed=0.4  # Slower escape maneuvers
        )
        
        # Threading and state management
        self._running = False
        self._threads = []
        self._mode = ControlMode.AUTO
        self._mode_lock = threading.Lock()
        self._emergency_stop = threading.Event()
        
        # Control parameters
        self.control_rate = 20  # Hz
        self.monitor_rate = 10  # Hz
        self.manual_deadzone = 0.1
        self.max_linear_speed = 0.8
        self.max_angular_speed = 0.6

    @property
    def mode(self) -> ControlMode:
        """Thread-safe mode access"""
        with self._mode_lock:
            return self._mode

    @mode.setter
    def mode(self, value: ControlMode):
        """Thread-safe mode setting"""
        with self._mode_lock:
            old_mode = self._mode
            self._mode = value
            if old_mode != value:
                logger.info(f"Mode changed from {old_mode.name} to {value.name}")
                self._on_mode_change(old_mode, value)

    def start_mission(self) -> bool:
        """Start all mission systems with obstacle avoidance"""
        if self._running:
            logger.warning("Mission already running")
            return False

        logger.info("Starting mission control with obstacle avoidance")
        self._running = True
        self._emergency_stop.clear()

        # Start component threads
        threads_to_start = [
            (self._autonomous_control_loop, "AutonomousControl"),
            (self._gamepad_monitor, "GamepadMonitor"),
            (self._safety_monitor, "SafetyMonitor"),
            (self._obstacle_avoidance_thread, "ObstacleAvoidance")  # New thread
        ]

        try:
            for target, name in threads_to_start:
                thread = threading.Thread(
                    target=target,
                    name=name,
                    daemon=True
                )
                thread.start()
                self._threads.append(thread)
                logger.info(f"Started {name} thread")

            # Watchdog thread
            watchdog = threading.Thread(
                target=self._watchdog,
                name="Watchdog",
                daemon=True
            )
            watchdog.start()
            self._threads.append(watchdog)

            return True

        except Exception as e:
            logger.critical(f"Mission start failed: {e}")
            self.stop_mission()
            return False

    def _autonomous_control_loop(self):
        """Main autonomous control thread with obstacle awareness"""
        control_interval = 1.0 / self.control_rate
        next_time = time.time()

        while self._running and not self._emergency_stop.is_set():
            try:
                if self.mode == ControlMode.AUTO:
                    self.follow_target.update()
                
                # Maintain precise timing
                next_time += control_interval
                sleep_time = next_time - time.time()
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    logger.warning(f"Control loop lagging by {-sleep_time:.3f}s")

            except Exception as e:
                logger.error(f"Autonomous control error: {e}")
                self._trigger_safety_hold()

    def _obstacle_avoidance_thread(self):
        """Dedicated thread for obstacle avoidance"""
        avoidance_interval = 0.1  # 10Hz
        
        while self._running and not self._emergency_stop.is_set():
            try:
                if self.mode in [ControlMode.AUTO, ControlMode.MANUAL]:
                    self.obstacle_avoidance.avoid_obstacles()
                time.sleep(avoidance_interval)
                
            except Exception as e:
                logger.error(f"Obstacle avoidance error: {e}")
                self._trigger_safety_hold()

    def _gamepad_monitor(self):
        """Gamepad input handling with mode control"""
        monitor_interval = 1.0 / self.monitor_rate

        while self._running and not self._emergency_stop.is_set():
            try:
                inputs = self.gamepad.get_input()
                
                # Mode toggle (using Triangle button as example)
                if inputs.get('triangle', False):
                    self._toggle_mode()
                
                # Emergency stop (using Circle button as example)
                if inputs.get('circle', False):
                    self._trigger_safety_hold()
                
                # Manual control
                if self.mode == ControlMode.MANUAL:
                    self._handle_manual_input(inputs)

                time.sleep(monitor_interval)

            except Exception as e:
                logger.error(f"Gamepad monitor error: {e}")
                time.sleep(1)

    def _handle_manual_input(self, inputs: Dict[str, float]):
        """Process manual control inputs with deadzone"""
        try:
            left_x = inputs.get('left_x', 0.0)
            left_y = inputs.get('left_y', 0.0)
            
            # Apply deadzone
            if abs(left_x) < self.manual_deadzone:
                left_x = 0.0
            if abs(left_y) < self.manual_deadzone:
                left_y = 0.0
                
            # Scale inputs
            forward = left_y * self.max_linear_speed
            turn = left_x * self.max_angular_speed
            
            self.drive_system.set_velocity(
                linear=forward,
                angular=turn
            )

        except Exception as e:
            logger.error(f"Manual control error: {e}")
            self.drive_system.stop()

    def _safety_monitor(self):
        """System health monitoring"""
        while self._running:
            try:
                if self._emergency_stop.is_set():
                    self.mode = ControlMode.SAFETY_HOLD
                    self.drive_system.emergency_stop()
                    time.sleep(1)
                    continue

                # Add additional safety checks here
                time.sleep(0.5)

            except Exception as e:
                logger.error(f"Safety monitor error: {e}")
                self._trigger_safety_hold()

    def _watchdog(self):
        """Thread health monitoring"""
        while self._running:
            dead_threads = [t.name for t in self._threads if not t.is_alive()]
            if dead_threads:
                logger.error(f"Critical threads dead: {dead_threads}")
                self._trigger_safety_hold()
            time.sleep(2)

    def _toggle_mode(self):
        """Toggle between AUTO and MANUAL modes"""
        if self.mode == ControlMode.SAFETY_HOLD:
            logger.warning("Cannot toggle mode while in safety hold")
            return

        new_mode = ControlMode.MANUAL if self.mode == ControlMode.AUTO else ControlMode.AUTO
        self.mode = new_mode

    def _trigger_safety_hold(self):
        """Initiate emergency procedures"""
        self._emergency_stop.set()
        logger.critical("SAFETY HOLD ACTIVATED")

    def _on_mode_change(self, old_mode: ControlMode, new_mode: ControlMode):
        """Handle mode transition logic"""
        self.drive_system.stop()
        
        if new_mode == ControlMode.AUTO:
            logger.info("Initializing autonomous systems")
            self.follow_target.reset()
            self.obstacle_avoidance.reset()

    def stop_mission(self):
        """Graceful shutdown procedure"""
        if not self._running:
            return

        logger.info("Stopping mission control")
        self._running = False
        self._emergency_stop.set()

        # Wait for threads to finish
        for t in self._threads:
            if t.is_alive():
                t.join(timeout=1.0)
                if t.is_alive():
                    logger.warning(f"Thread {t.name} failed to stop")

        self.drive_system.stop()
        logger.info("Mission stopped cleanly")

    def __enter__(self):
        """Context manager entry"""
        self.start_mission()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_mission()