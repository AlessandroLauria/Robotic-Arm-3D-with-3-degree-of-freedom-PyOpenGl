import math
import matplotlib.pyplot as plt

GRAVITY = 9.81

class Pendolo:

    def __init__(self, _M, _b):
        self.w = 0
        self.theta = 0
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



class PIDSat:

    def __init__(self, kp, ki, kd, sat):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.saturation = sat
        self.integral = 0
        self.prev_error = 0
        self.saturation_flag = False

    def evaluate(self, target, current, delta_t):
        error = target - current
        if not(self.saturation_flag):
            self.integral = self.integral + error * delta_t
        deriv = (error - self.prev_error) / delta_t
        self.prev_error = error
        output = self.kp * error + self.ki * self.integral + self.kd * deriv
        if output > self.saturation:
            output = self.saturation
            self.saturation_flag = True
        elif output < -self.saturation:
            output = -self.saturation
            self.saturation_flag = True
        else:
            self.saturation_flag = False
        return output



class ProfilePositionController:

    def __init__(self, max_speed, accel, decel):
        self.__accel = accel
        self.__max_speed = max_speed
        self.__decel = decel
        self.__decel_distance = max_speed * max_speed / (2.0 * decel)
        self.__output_speed = 0 # la velocita' a cui andremo

    def evaluate(self, target_position, current_position,\
   current_speed, delta_t):
        distance = target_position - current_position

        # calcoliamo il segno e usiamo distanze sempre positive
        if distance >= 0:
            s = 1
        else:
            s = -1
            distance = -distance

        if distance < self.__decel_distance:
            # ok siamo nella fase di decelerazione
            vel_attesa = \
  math.sqrt(self.__max_speed * self.__max_speed - \
                          2 * self.__decel * \
   (self.__decel_distance - distance))
            if vel_attesa > self.__output_speed:
                # uhm... strana condizione,
                # vuol dire che siamo ancora in accelerazione (fase 1)
                # continuiamo ad accelerare
                self.__output_speed += self.__accel * delta_t
                # controlliamo se abbiamo comunque raggiunto
                # (e superato) la velocita' attesa
                if self.__output_speed > vel_attesa:
                    self.__output_speed = vel_attesa
                # evitiamo anche di superare la velocita' massima
                if self.__output_speed > self.__max_speed:
                    self.__output_speed = self.__max_speed
            else:
                # qui siamo effettivamente in decelerazione
                self.__output_speed = vel_attesa

        else:
            # non siamo nella fase di decelerazione quindi...
            if self.__output_speed < self.__max_speed:
                # se non siamo gia' a velocita' massima, acceleriamo
                self.__output_speed += self.__accel * delta_t
                # ma evitiamo sempre di superare la velocita' massima
                if self.__output_speed > self.__max_speed:
                    self.__output_speed = self.__max_speed

        # applichiamo il segno
        return s * self.__output_speed


L1 = 8
L2 = 2


def cinematica_inversa(Xt, Yt, alpha_t):

    th2 = math.atan2(math.sqrt(abs(1-((Xt**2 + Yt**2 - L1**2 - L2**2)/2*L1*L2)**2)), (Xt**2 + Yt**2 - L1**2 - L2**2)/2*L1*L2)
    th1 = math.atan2(Yt,Xt) - math.atan2(L2*math.sin(th2), L1 + L2*math.cos(th2))
    th3 = alpha_t - th1 - th2

    th1 = math.degrees(th1)
    th2 = math.degrees(th2)
    th3 = math.degrees(th3)

    return th1, th2, th3

#Input in gradi
def cinematica_diretta(th1, th2, th3):
    th1 = math.radians(th1)
    th2 = math.radians(th2)
    th3 = math.radians(th3)
    x = L1*math.cos(th1) + L2*math.cos(th1+th2)
    y = L1*math.sin(th1) + L2*math.sin(th1+th2)
    alpha = th1 + th2 + th3
    return x, y, alpha


delta_t = 1e-3 # 1 ms

joint_1 = Pendolo(6.0, 4.0)
joint_2 = Pendolo(6.0, 4.0)
joint_3 = Pendolo(6.0, 4.0)

speed_controller_1 = PIDSat(10000, 20000, 0, 100)
speed_controller_2 = PIDSat(10000, 20000, 0, 100)
speed_controller_3 = PIDSat(10000, 20000, 0, 100)

position_controller_1 = ProfilePositionController(5, 0.02, 0.02)
position_controller_2 = ProfilePositionController(5, 0.02, 0.02)
position_controller_3 = ProfilePositionController(5, 0.02, 0.02)

t = 0.0

target_1, target_2, target_3 = cinematica_inversa(5, 6, 0)

print(target_1, " ", target_2, " ", target_3)

th1 = []
th2 = []
th3 = []
time = []

current_x = []
current_y = []

while t < 400:

    x, y, alpha = cinematica_diretta(joint_1.theta, joint_2.theta, joint_3.theta)

    w_target_1 = position_controller_1.evaluate(target_1, joint_1.theta, joint_1.w, delta_t)
    w_target_2 = position_controller_2.evaluate(target_2, joint_2.theta, joint_2.w, delta_t)
    w_target_3 = position_controller_3.evaluate(target_3, joint_3.theta, joint_3.w, delta_t)

    output_1 = speed_controller_1.evaluate(w_target_1, joint_1.w, delta_t)
    output_2 = speed_controller_2.evaluate(w_target_2, joint_2.w, delta_t)
    output_3 = speed_controller_3.evaluate(w_target_3, joint_3.w, delta_t)

    joint_1.evaluate(output_1, delta_t)
    joint_2.evaluate(output_2, delta_t)
    joint_3.evaluate(output_3, delta_t)

    current_x.append(x)
    current_y.append(y)

    t = t + delta_t

    th1.append(joint_1.theta)
    th2.append(joint_2.theta)
    th3.append(joint_3.theta)
    time.append(t)

print(current_x[-1], " ", current_y[-1])
plt.plot(time, th1, label='th1')
plt.xlabel('time')
plt.legend()
plt.show()

plt.plot(time, th2, label='th2')
plt.xlabel('time')
plt.legend()
plt.show()

plt.plot(time, th3, label='th3')
plt.xlabel('time')
plt.legend()
plt.show()

plt.plot(current_x, current_y, label='posizione')
plt.xlabel('x')
plt.legend()
plt.show()