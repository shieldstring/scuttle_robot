class SpeedControl:
    def __init__(self):
        self.target_speed = 0.0

    def set_target_speed(self, speed):
        self.target_speed = speed

    def compute_duty_cycle(self, current_speed):
        # Simple proportional control
        error = self.target_speed - current_speed
        duty_cycle = error * 0.5  # Proportional gain
        return duty_cycle