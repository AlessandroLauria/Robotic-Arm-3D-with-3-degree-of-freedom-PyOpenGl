from RobotArm import *

target = Target(2, 3, 5)
#Per fare la conversione diretta, inversa, computare l'angolo di rotazione per la z. Prende in input la lunghezza delle braccia.
kinematics = Kinematics(2, 2, 2)
app = RobotArm(target, kinematics, alpha = 1.54)
app.run()