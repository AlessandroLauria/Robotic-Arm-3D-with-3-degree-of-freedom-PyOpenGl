import math

class Convert:
    def __init__(self):
        print()

    # convert in radiant
    def from_degrees_to_rad(self, angle):
        return angle * math.pi / 180

    # convert in degrees
    def from_rad_to_degrees(self, angle):
        return angle * 180 / math.pi