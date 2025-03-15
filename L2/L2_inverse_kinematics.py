class InverseKinematics:
    def __init__(self, wheelbase):
        self.wheelbase = wheelbase

    def compute_wheel_speeds(self, x_dot, theta_dot):
        phiL = x_dot - theta_dot * self.wheelbase / 2
        phiR = x_dot + theta_dot * self.wheelbase / 2
        return phiL, phiR