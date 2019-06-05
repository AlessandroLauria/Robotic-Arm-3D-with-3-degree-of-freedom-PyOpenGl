import math

class FollowTarget:

    def __init__(self, l1, l2, th1, th2, th3):
        # Arm lenghts
        self.l1 = l1
        self.l2 = l2
        # Arm angles
        self.th1 = th1
        self.th2 = th2
        self.th3 = th3
        # target point coordinates
        self.target_x = 0
        self.target_y = 0
        self.target_z = 0

    # set target point coordinates
    def set_target(self, x, y, z=0):
        self.target_x = x
        self.target_y = y
        self.target_z = z

    # update angles to get the target in 2d
    def follow_target_2d(self, th1, th2, th3, target_x, target_y):
        th2 = math.atan2(
                    math.sqrt(1 - ((target_x**2 + target_y**2 - self.l1**2 - self.l2**2)/(2*self.l1*self.l2)**2)),
                    (target_x ** 2 + target_y ** 2 - self.l1 ** 2 - self.l2 ** 2) / (2 * self.l1 * self.l2) ** 2
                    )
        th1 = math.atan2(target_x, target_y) - math.atan2(self.l2*math.sin(th2), self.l1 + self.l2*math.cos(th2))

        #FIX ME: aggiungere th3, al momento sto provando solo con th1
        return th1, th2, th3