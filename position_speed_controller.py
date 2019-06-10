import pylab
import math

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
            vel_attesa = math.sqrt(self.__max_speed * self.__max_speed - 2 * self.__decel * (self.__decel_distance - distance))
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


delta_t = 1e-3 # 1 ms

braccio = Pendolo(6.0, 4.0)

speed_controller = PIDSat(10000, 20000, 0, 100)
position_controller = ProfilePositionController(0.1, 0.02, 0.02)

t = 0.0

target = math.radians(180)

vettore_theta = [ ]
vettore_w = [ ]
vettore_wt = [ ]
vettore_tempi = [ ]
vettore_output = [ ]

while t < 50:

    w_target = position_controller.evaluate(target, braccio.theta, braccio.w, delta_t)

    output = speed_controller.evaluate(w_target, braccio.w, delta_t)
    braccio.evaluate(output, delta_t)

    t = t + delta_t

    vettore_w.append(braccio.w)
    vettore_wt.append(w_target)
    vettore_theta.append(math.degrees(braccio.theta))
    vettore_output.append(output)
    vettore_tempi.append(t)


pylab.figure(1)
pylab.plot(vettore_tempi, vettore_wt, 'b-+', label='target, w(t)')
pylab.plot(vettore_tempi, vettore_w, 'r-+', label='vel, w(t)')
pylab.xlabel('time')
pylab.legend()

pylab.figure(2)
pylab.plot(vettore_tempi, vettore_theta, 'b-+', label='position, theta(t)')
pylab.xlabel('time')
pylab.legend()

pylab.figure(3)
pylab.plot(vettore_tempi, vettore_output, 'b-+', label='force')
pylab.xlabel('time')
pylab.legend()

pylab.show()
