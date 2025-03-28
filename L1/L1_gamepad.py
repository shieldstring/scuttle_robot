import pygame
import logging
import time

class Gamepad:
    def __init__(self, retry_interval=1, max_retries=5):
        pygame.init()
        pygame.joystick.init()
        self.joystick = None
        self.retry_interval = retry_interval
        self.max_retries = max_retries
        self._initialize_gamepad()

    def _initialize_gamepad(self):
        """Initialize gamepad with retry logic"""
        for attempt in range(self.max_retries):
            try:
                if pygame.joystick.get_count() > 0:
                    self.joystick = pygame.joystick.Joystick(0)
                    self.joystick.init()
                    logging.info(f"Gamepad connected: {self.joystick.get_name()}")
                    return
                else:
                    logging.warning(f"No gamepad detected (attempt {attempt + 1}/{self.max_retries})")
            except Exception as e:
                logging.error(f"Initialization error: {str(e)}")
            
            time.sleep(self.retry_interval)
        
        raise RuntimeError("Failed to initialize gamepad after multiple attempts")

    def get_input(self):
        """Get normalized input from gamepad with deadzone handling"""
        if not self.joystick:
            raise RuntimeError("Gamepad not initialized")
        
        try:
            pygame.event.pump()
            
            # Add deadzone threshold (adjust as needed)
            deadzone = 0.1
            
            # Get axis values with deadzone filtering
            x_axis = self._apply_deadzone(self.joystick.get_axis(0), deadzone)
            y_axis = self._apply_deadzone(self.joystick.get_axis(1), deadzone)
            
            logging.debug(f"Gamepad input - X: {x_axis:.2f}, Y: {y_axis:.2f}")
            return x_axis, y_axis
            
        except Exception as e:
            logging.error(f"Input error: {str(e)}")
            raise

    def _apply_deadzone(self, value, threshold):
        """Apply deadzone to axis values"""
        if abs(value) < threshold:
            return 0.0
        return value

    def __del__(self):
        if self.joystick:
            self.joystick.quit()
        pygame.quit()