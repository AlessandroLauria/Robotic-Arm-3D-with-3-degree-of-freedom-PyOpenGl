import math

class Kinematics:

    def __init__(self):
        self.L1 = 2
        self.L2 = 2
        self.L3 = 2

    def __init__(self, L1, L2, L3):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3

    def inverse_kinematics(self, Xt, Yt, alpha_t):
        num = ((math.pow(Xt, 2) + math.pow(Yt, 2) - math.pow(self.L1, 2) - math.pow(self.L2, 2)) / (2 * self.L1 * self.L2))
        diff = 1 - (math.pow(num, 2))
        if diff < 0:
            diff = 0
        th2 = math.atan2(math.sqrt(diff), num)
        th1 = math.atan2(Yt, Xt) - math.atan2(self.L2 * math.sin(th2), self.L1 + self.L2 * math.cos(th2))
        th3 = alpha_t - th1 - th2

        th1 = math.degrees(th1)
        th2 = math.degrees(th2)
        th3 = math.degrees(th3)

        return th1, th2, th3

    # Input in gradi
    def direct_kinematics(self, th1, th2, th3):
        th1 = math.radians(th1)
        th2 = math.radians(th2)
        th3 = math.radians(th3)
        x = self.L1 * math.cos(th1) + self.L2 * math.cos(th1 + th2) + self.L3 * math.cos(th1 + th2 + th3)
        y = self.L1 * math.sin(th1) + self.L2 * math.sin(th1 + th2) + self.L3 * math.sin(th1 + th2 + th3)
        alpha = th1 + th2 + th3
        return x, y, alpha


    def compute_theta_z(self, target_x, target_z):
        if target_z == 0:
            return 0
        h = math.hypot(target_x, target_z)
        num = (pow(h, 2) + pow(target_x, 2) - pow(target_z, 2))
        try:
            cos_alpha = num / (2 * h * target_x)
        except:
            if target_x == 0 and target_z != 0:
                cos_alpha = 0
            else:
                cos_alpha = 1

        #print(cos_alpha)
        alpha = math.acos(cos_alpha)
        alpha = math.degrees(alpha)
        return alpha