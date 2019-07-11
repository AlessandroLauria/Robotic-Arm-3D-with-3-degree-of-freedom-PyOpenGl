from RobotArm import *
target = Target(-4, 3, -3)
#Per fare la conversione diretta, inversa, computare l'angolo di rotazione per la z. Prende in input la lunghezza delle braccia.
conversion = ConversionFunction(2, 2, 2)
app = RobotArm(target, conversion)
app.run()