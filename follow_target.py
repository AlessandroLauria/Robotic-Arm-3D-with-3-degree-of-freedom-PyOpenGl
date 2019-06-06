import math
from convert import Convert

cnv = Convert()

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

        # We need radiant angles to perform operations
        th1 = cnv.from_degrees_to_rad(th1)
        th2 = cnv.from_degrees_to_rad(th2)
        th3 = cnv.from_degrees_to_rad(th3)

        th2 = math.atan2(
                    math.sqrt(abs(1 - ((target_x**2 + target_y**2 - self.l1**2 - self.l2**2)/(2*self.l1*self.l2)**2))),
                    (target_x ** 2 + target_y ** 2 - self.l1 ** 2 - self.l2 ** 2) / (2 * self.l1 * self.l2) ** 2
                    )
        th1 = math.atan2(target_x, target_y) - math.atan2(self.l2*math.sin(th2), self.l1 + self.l2*math.cos(th2))

        th3 = th3 - th1 - th2

        # Convert the results in degrees and return
        th1 = cnv.from_rad_to_degrees(th1)
        th2 = cnv.from_rad_to_degrees(th2)
        th3 = cnv.from_rad_to_degrees(th3)

        print("[follow target] th: ", th1, th2, th3)

        return th1, th2, th3