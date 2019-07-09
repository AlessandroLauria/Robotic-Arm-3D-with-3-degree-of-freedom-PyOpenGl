class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev_error = 0

    def evaluate(self, error, delta_t):
        deriv = (error - self.prev_error) / delta_t
        self.prev_error = error
        self.integral = self.integral + error * delta_t
        output = self.kp * error + self.ki * self.integral + self.kd * deriv
        return output