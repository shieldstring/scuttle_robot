import pygame
import logging
import time
from typing import Tuple, Optional

class Gamepad:
    def __init__(self, retry_interval=1, max_retries=5):
        self.logger = logging.getLogger('gamepad')
        self.joystick = None
        self.retry_interval = retry_interval
        self.max_retries = max_retries
        self._initialize()

    def _initialize(self):
        """Initialize with comprehensive diagnostics"""
        pygame.init()
        pygame.joystick.init()
        
        for attempt in range(1, self.max_retries + 1):
            try:
                count = pygame.joystick.get_count()
                self.logger.info(f"Detected {count} gamepad(s)")
                
                if count > 0:
                    self.joystick = pygame.joystick.Joystick(0)
                    self.joystick.init()
                    
                    # Print gamepad info
                    self.logger.info(
                        f"Connected: {self.joystick.get_name()}\n"
                        f"Axes: {self.joystick.get_numaxes()}\n"
                        f"Buttons: {self.joystick.get_numbuttons()}"
                    )
                    
                    # Test axis response
                    pygame.event.pump()
                    self.logger.debug("Initial axis values:")
                    for i in range(self.joystick.get_numaxes()):
                        self.logger.debug(f"Axis {i}: {self.joystick.get_axis(i):.2f}")
                    return
                
            except Exception as e:
                self.logger.error(f"Init error (attempt {attempt}): {str(e)}")
            
            time.sleep(self.retry_interval)
        
        raise RuntimeError("Gamepad not found")

    def get_input(self) -> Tuple[float, float]:
        """Get normalized (x,y) input from left stick"""
        if not self.joystick:
            raise RuntimeError("Gamepad not initialized")
        
        pygame.event.pump()
        
        # Common mappings - may need adjustment for your gamepad
        left_x = self._filter_axis(self.joystick.get_axis(0))  # Left stick X
        left_y = -self._filter_axis(self.joystick.get_axis(1)) # Left stick Y (inverted)
        
        return left_x, left_y

    def _filter_axis(self, value: float, deadzone: float = 0.1) -> float:
        """Apply deadzone and scale output"""
        if abs(value) < deadzone:
            return 0.0
        return value * 1.0  # Remove this multiplier if too sensitive

    def __del__(self):
        if self.joystick:
            self.joystick.quit()
        pygame.quit()