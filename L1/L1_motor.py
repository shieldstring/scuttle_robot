import gpiozero

class MotorController:
    def __init__(self, pins):
        self.motor_a = gpiozero.PWMOutputDevice(pins[0])
        self.motor_b = gpiozero.PWMOutputDevice(pins[1])
        self.motor_c = gpiozero.PWMOutputDevice(pins[2])
        self.motor_d = gpiozero.PWMOutputDevice(pins[3])

    def set_speed(self, duty_cycle):
        self.motor_a.value = duty_cycle[0]
        self.motor_b.value = duty_cycle[1]
        self.motor_c.value = duty_cycle[2]
        self.motor_d.value = duty_cycle[3]