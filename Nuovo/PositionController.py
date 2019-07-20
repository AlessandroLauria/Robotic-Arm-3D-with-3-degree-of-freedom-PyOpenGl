import math
class PositionController:

    def __init__(self, max_speed, accel, decel):
        self.__accel = accel
        self.__max_speed = max_speed
        self.__decel = decel
        self.__decel_distance = max_speed * max_speed / (2.0 * decel)
        self.__output_speed = 0 # la velocita' a cui andremo

    def evaluate(self, target_position, current_position,\
        delta_t):
        distance = target_position - current_position

        if distance >= 0:
            s = 1
        else:
            s = -1
            distance = -distance

        if distance < self.__decel_distance:
            # decelartion
            vel_attesa = \
              math.sqrt(self.__max_speed * self.__max_speed - \
                          2 * self.__decel * \
                (self.__decel_distance - distance))
            if vel_attesa > self.__output_speed:
                # Still in acceleration phase
                self.__output_speed += self.__accel * delta_t
                # controlliamo se abbiamo comunque raggiunto
                # (e superato) la velocita' attesa
                if self.__output_speed > vel_attesa:
                    self.__output_speed = vel_attesa
                # evitiamo anche di superare la velocita' massima
                if self.__output_speed > self.__max_speed:
                    self.__output_speed = self.__max_speed
            else:
                # deceleration phase
                self.__output_speed = vel_attesa

        else:
            # aceleration phase
            if self.__output_speed < self.__max_speed:
                # if we are not already a maximum speed, we accelerate
                self.__output_speed += self.__accel * delta_t
                # but we always avoid exceeding the maximum speed
                if self.__output_speed > self.__max_speed:
                    self.__output_speed = self.__max_speed

        # apply sign
        return s * self.__output_speed

