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

