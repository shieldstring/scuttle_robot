import pygame

class Gamepad:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def get_input(self):
        pygame.event.pump()
        x_axis = self.joystick.get_axis(0)  # Left stick X-axis
        y_axis = self.joystick.get_axis(1)  # Left stick Y-axis
        return x_axis, y_axis