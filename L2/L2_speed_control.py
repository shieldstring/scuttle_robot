import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

class SpeedControl:
    def __init__(self):
        self.target_speed = 0.0

    def set_target_speed(self, speed):
        """
        Set the target speed for the robot.
        """
        self.target_speed = speed
        logging.debug(f"Target speed set to: {speed}")

    def compute_duty_cycle(self, current_speed):
        """
        Compute the duty cycle based on the current speed.
        """
        try:
            error = self.target_speed - current_speed
            duty_cycle = error * 0.5  # Proportional gain
            logging.debug(f"Duty cycle computed: {duty_cycle}")
            return duty_cycle
        except Exception as e:
            logging.error(f"An error occurred while computing duty cycle: {e}")
            raise