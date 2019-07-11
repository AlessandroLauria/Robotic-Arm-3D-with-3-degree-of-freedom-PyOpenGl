from RobotArm import *

target = Target(0, 4, 0)
#Per fare la conversione diretta, inversa, computare l'angolo di rotazione per la z. Prende in input la lunghezza delle braccia.
kinematics = Kinematics(2, 2, 2)
app = RobotArm(target, kinematics)
app.run()