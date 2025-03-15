class OnboardSystem:
    def __init__(self):
        self.battery_voltage = 0.0

    def update_battery_status(self, voltage):
        self.battery_voltage = voltage