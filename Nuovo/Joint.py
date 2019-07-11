GRAVITY = 9.81
import math

class Joint:

    def __init__(self, _M, _b, theta):
        self.w = 0
        self.theta = theta
        self.M = _M
        self.b = _b


    def evaluate(self, _input, delta_t):
        w_temp = self.w - GRAVITY * delta_t * math.sin(self.theta) - \
            self.b * delta_t * self.w / self.M + \
            delta_t * _input / self.M
        self.theta = self.theta + delta_t * self.w
        self.w = w_temp

        return

        if self.theta > math.pi:
            self.theta = self.theta - 2*math.pi
        if self.theta < -math.pi:
            self.theta = 2*math.pi + self.theta

