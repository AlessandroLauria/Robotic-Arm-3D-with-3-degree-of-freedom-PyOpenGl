#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
from convert import *

cnv = Convert()
L1 = 3
L2 = 3

#Posizione attuale
Xc = 0
Yc = 0
alpha_c = 0

#Posizione Target
Xt = 6
Yt = 0
alpha_t = 1.57

#Output in gradi.
def cinematica_inversa(Xt, Yt, alpha_t):

    th2 = math.atan2(math.sqrt(abs(1-((Xt**2 + Yt**2 - L1**2 - L2**2)/2*L1*L2)**2)), (Xt**2 + Yt**2 - L1**2 - L2**2)/2*L1*L2)
    th1 = math.atan2(Yt,Xt) - math.atan2(L2*math.sin(th2), L1 + L2*math.cos(th2))
    th3 = alpha_t - th1 - th2
    #print("Cinematica invera prima: th1-->", th1, ", th2-->", th2,", th3-->", th3)

    th1 = cnv.from_rad_to_degrees(th1)
    th2 = cnv.from_rad_to_degrees(th2)
    th3 = cnv.from_rad_to_degrees(th3)
    #print("Cinematica inversa dopo: th1-->", th1, ", th2-->", th2,", th3-->", th3)

    return th1, th2, th3


#Input in gradi
def cinematica_diretta(th1, th2, th3):
   # print("Cinematica diretta prima: th1-->", th1, ", th2-->", th2,", th3-->", th3)
    th1 = cnv.from_degrees_to_rad(th1)
    th2 = cnv.from_degrees_to_rad(th2)
    th3 = cnv.from_degrees_to_rad(th3)
    #print("Cinematica diretta dopo: th1-->", th1, ", th2-->", th2,", th3-->", th3)
    Xt = L1*math.cos(th1) + L2*math.cos(th1+th2)
    Yt = L1*math.sin(th1) + L2*math.sin(th1+th2)
    alpha_t = th1 + th2 + th3
    return Xt, Yt, alpha_t




class PISat:

    def __init__(self, kp, ki, sat):
        self.kp = kp
        self.ki = ki
        self.saturation = sat
        self.integral = 0
        self.saturation_flag = False

    def evaluate(self, target, current, delta_t):
        error = target - current
        if not(self.saturation_flag):
            self.integral = self.integral + error * delta_t
        output = self.kp * error + self.ki * self.integral
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

    def evaluate(self, target_position, current_position, current_speed, delta_t):
        distance = target_position - current_position

        # calcoliamo il segno e usiamo distanze sempre positive
        if distance >= 0:
            s = 1
        else:
            s = -1
            distance = -distance

        if distance < self.__decel_distance:
            # ok siamo nella fase di decelerazione
            vel_attesa = math.sqrt(self.__max_speed * self.__max_speed - \
                                   2 * self.__decel * (self.__decel_distance - distance))
            if vel_attesa > self.__output_speed:
                # uhm... strana condizione,
                # vuol dire che siamo ancora in accelerazione (fase 1)
                # continuiamo ad accelerare
                self.__output_speed += self.__accel * delta_t
                # controlliamo se abbiamo comunque raggiunto (e superato) la velocita' attesa
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

speed_controller = PISat(1,0,1000)
position_controller = ProfilePositionController(500, 100, 100)

# Angoli e velocità corrente
current_th1 = 0
current_th2 = 0
current_th3 = 0
current_speed_1 = 0
current_speed_2 = 0
current_speed_3 = 0

t = 0
delta_t = 0.001


# Angoli target dalla cinematica inversa:
target_th1, target_th2, target_th3 = cinematica_inversa(Xt, Yt, alpha_t)


x_current = []
y_current = []
x_target = []
y_target = []

th1_plot = []
th2_plot = []
th3_plot = []

time = []

while t < 5:

    x_current_provv, y_current_provv, alpha_c = cinematica_diretta(current_th1, current_th2, current_th3)
    #print("Giro numero: ", len(time), " -->",x_current_provv, y_current_provv, alpha_c, " con angoli th1, th2, th3 -->", current_th1, current_th2, current_th3)
    #target_th1, target_th2, target_th3 = cinematica_inversa(Xt, Yt, alpha_t)
    #print("Giro numero: ", len(time), " target th1, target th2, target th3 -->", target_th1, target_th2, target_th3)
    target_speed_1 = position_controller.evaluate(target_th1, current_th1, 0, delta_t)
    target_th1 = speed_controller.evaluate(target_speed_1, current_speed_1, delta_t)
    #print("Giro numero: ", len(time), " target_speed-1 = ", target_speed_1, ", curent_th1 aggiornato vale: ", current_th1)
    target_speed_2 = position_controller.evaluate(target_th2, current_th2, 0, delta_t)
    target_th2 = speed_controller.evaluate(target_speed_2, current_speed_2, delta_t)
    #print("Giro numero: ", len(time), " target_speed-2 = ", target_speed_2, ", curent_th2 aggiornato vale: ", current_th2)
    target_speed_3 = position_controller.evaluate(target_th3, current_th3, 0, delta_t)
    target_th3 = speed_controller.evaluate(target_speed_3, current_speed_3, delta_t)
    #print("Giro numero: ", len(time), " target_speed-3 = ", target_speed_3, ", curent_th1 aggiornato vale: ", current_th3)

    th1_plot.append(current_th1)
    th2_plot.append(current_th2)
    th3_plot.append(current_th3)
    x_current.append(x_current_provv)
    y_current.append(y_current_provv)
    x_target.append(Xt)
    y_target.append(Yt)
    t += delta_t
    time.append(t)


plt.plot(time, x_current, label='output')
plt.plot(time, y_current, label='riferimento')
plt.xlabel('time')
plt.legend()

plt.show()

plt.plot(time, th1_plot, label='th1')
plt.plot(time, th2_plot, label='th2')
plt.plot(time, th3_plot, label='th3')
plt.xlabel('time')
plt.legend()

plt.show()