# coding=utf-8



#TODO: Sistemare asse z -->
#TODO: Refactoring codice
#TODO: Disegnare target
#TODO: Decidere come gestire target non raggiungibili --> fare scaling del target.

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from vertices import *
from reach_target import *
from position_speed_controller import *
from controllers import *

from prova_alessandro import *
from time import sleep


class Target:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0

	def display(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

		glTranslatef(x, y, z)
		glRotatef(90.0, 0.0, 0.0, 1.0)
		glTranslatef(1.0, -1.0, 0.0)
		glPushMatrix()
		glScalef(1.0, 0.2, 0.5)
		Parallelepiped(vertices_target)
		glPopMatrix()


	
class SimpleRobotArm:

	def __init__(self):
		self.name= "Simple Robot Arm"
		self.shoulder = 90.0
		self.elbow = 0.0
		self.arm = 0.0

		# Class that handle "follow target" algorithm
		self.fl = ReachTarget(3,3,self.shoulder,self.elbow,self.arm)

		# Class that draw the target
		#self.target = Target()

	def run(self):
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

		glutInitWindowSize(1000,1000)
		glutInitWindowPosition(100,100)
		glutCreateWindow(self.name)

		glClearColor(0.0,0.0,0.0,0.0)
		glShadeModel(GL_FLAT)

		glutDisplayFunc(self.display)
		glutReshapeFunc(self.reshape)
		glutKeyboardFunc(self.keys)

		# Update shoulder, elbow and arm thetas to follow the target
		# self.shoulder, self.elbow, self.arm = self.fl.reach_target_2d(self.shoulder, self.elbow, self.arm, 10, -10)

		glutMainLoop()

	def display(self):
		#self.shoulder, self.elbow, self.arm = self.fl.follow_target_2d(self.shoulder, self.elbow, self.arm, 100, 30)



		glClear(GL_COLOR_BUFFER_BIT)
		glPushMatrix()
		glTranslatef(0.0, -3.0, -3.0)
		glRotatef(self.shoulder, 0.0, 0.0, 1.0)
		glTranslatef(1.0, 0.0, 0.0)
		glPushMatrix()
		glScalef(1.0, 0.2, 0.5)
		Parallelepiped(vertices_1)
		glPopMatrix()

		glTranslatef(1.0, 0.0, 0.0)
		glRotatef(self.elbow, 0.0, 0.0, 0.8)
		glTranslatef(1.0, -0.8, 0.0)
		glPushMatrix()
		glScalef(1.0, 0.2, 0.5)
		Parallelepiped(vertices_2)
		glPopMatrix()

		glTranslatef(1.0, 0.0, 0.0)
		glRotatef(self.arm, 0.0, 0.0, 1.0)
		glTranslatef(1.0, -0.8, 0.0)
		glPushMatrix()
		glScalef(1.0, 0.2, 0.5)
		Parallelepiped(vertices_3)
		glPopMatrix()
		#self.target.display(- 2,3,1)
		glPopMatrix()
		glutSwapBuffers()


	def keys(self, *args):
		key = args[0]
		if (key == b'z'):
			self.shoulder = (self.shoulder+5) % 360
		elif (key==b'x'):
			self.shoulder = (self.shoulder-5) % 360
		elif (key==b'a'):
			self.elbow = (self.elbow+5) % 360
		elif (key==b's'):
			self.elbow = (self.elbow-5) % 360
		elif (key==b'q'):
			self.arm = (self.arm+5) % 360
		elif (key==b'w'):
			self.arm = (self.arm-5) % 360
		elif(key==b'e'):
			glRotatef(1.0, 0.0, 0.0, 0.0)
		elif (key == b'l'):
			self.shoulder, self.elbow, self.arm = self.fl.reach_target_2d(self.shoulder, self.elbow, self.arm, 100, -100)
		elif (key == b'p'):
			self.shoulder = 90.0
			self.elbow = 0.0
			self.arm = 0.0
		elif (key == b't'):
			self.follow_target_slowly(100, -100)
		elif (key == b'c'):
			self.follow_target_controller(100, -100)
		glutPostRedisplay()

	def reshape(self, w, h):
		glViewport (0, 0, w, h)
		glMatrixMode (GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(65.0, w/h, 1.0, 20.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslatef (0.0, 0.0, -6.0)


	def follow_target_slowly(self, target_x_final, target_y_final, target_z_final = 0):
		'''final_shoulder, final_elbow, final_arm = self.fl.reach_target_2d(self.shoulder, self.elbow, self.arm, target_x_final, target_y_final)
		final_shoulder = round(final_shoulder, 1)
		final_elbow = round(final_elbow, 1)
		final_arm = round(final_arm, 1)

		controller_shoulder = PID(2,0,0)
		controller_elbow = PID(2,0,0)
		controller_arm = PID(2,0,0)

		dt = 0.1
		t = 0
		while t < 20:
			self.shoulder = round(self.shoulder, 1)
			self.elbow = round(self.elbow, 1)
			self.arm = round(self.arm, 1)
			if self.shoulder < final_shoulder:
				self.shoulder += 0.1
			elif self.shoulder > final_shoulder:
				self.shoulder -= 0.1
			if self.elbow < final_elbow:
				self.elbow += 0.1
			elif self.elbow > final_elbow:
				self.elbow -= 0.1
			if self.arm < final_arm:
				self.arm += 0.1
			elif self.arm > final_arm:
				self.arm -= 0.1
			print("self.arm: ", self.arm, "self.elbow", self.elbow, "self.shoulder", self.shoulder)
			final_shoulder, final_elbow, final_arm = self.fl.reach_target_2d(self.shoulder, self.elbow, self.arm, target_x_final, target_y_final)

			self.arm = controller_arm.evaluate(final_arm - (self.arm%360-180), dt)
			self.elbow = controller_elbow.evaluate(final_elbow - (self.elbow%360-180), dt)
			self.shoulder = controller_shoulder.evaluate(final_shoulder - (self.shoulder%360-180), dt)

			if self.arm == final_arm and self.elbow == final_elbow and self.shoulder == final_shoulder:
				break

			t += 1
			self.display()'''

		delta_t = 1e-3  # 1 ms

		joint_1 = Pendolo(6.0, 4.0)
		joint_2 = Pendolo(6.0, 4.0)
		joint_3 = Pendolo(6.0, 4.0)

		speed_controller_1 = PIDSat(10000, 20000, 0, 100)
		speed_controller_2 = PIDSat(10000, 20000, 0, 100)
		speed_controller_3 = PIDSat(10000, 20000, 0, 100)

		position_controller_1 = ProfilePositionController(20, 5, 5)
		position_controller_2 = ProfilePositionController(20, 5, 5)
		position_controller_3 = ProfilePositionController(20, 5, 5)

		t = 0.0

		x, y, alpha = cinematica_diretta(90, 0, 0)
		print("Punto-->", x, y, alpha)
		target_1, target_2, target_3 = cinematica_inversa(0, 8, 1.57)

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
			self.shoulder = joint_1.theta
			self.elbow = joint_2.theta
			self.arm = joint_3.theta
			self.display()
			#th1.append(joint_1.theta)
			#th2.append(joint_2.theta)
			#th3.append(joint_3.theta)

			time.append(t)

	def follow_target_controller(self, target_x_final, target_y_final, target_z_final = 0):
		delta_t = 1e-3 # 1 ms

		shoulder = Braccio(6.0, 4.0, self.shoulder)
		elbow = Braccio(6.0, 4.0, self.elbow)
		arm = Braccio(6.0, 4.0, self.arm)

		speed_controller = PIDSat(10000, 20000, 0, 100)
		position_controller = ProfilePositionController(0.1, 0.02, 0.02)

		t = 0.0

		finalShoulder, finalElbow, finalArm = self.fl.reach_target_2d(self.shoulder, self.elbow, self.arm, target_x_final, target_y_final)

		while t < 10:

		    w_target_S = position_controller.evaluate(finalShoulder, shoulder.theta, shoulder.w, delta_t)
		    w_target_E = position_controller.evaluate(finalElbow, elbow.theta, elbow.w, delta_t)
		    w_target_A = position_controller.evaluate(finalArm, arm.theta, arm.w, delta_t)

		    output_S = speed_controller.evaluate(w_target_S, shoulder.w, delta_t)
		    output_E = speed_controller.evaluate(w_target_E, elbow.w, delta_t)
		    output_A = speed_controller.evaluate(w_target_A, arm.w, delta_t)
		    
		    shoulder.evaluate(output_S, delta_t)
		    elbow.evaluate(output_E, delta_t)
		    arm.evaluate(output_A, delta_t)

		    self.shoulder = shoulder.theta
		    self.elbow = elbow.theta
		    self.arm = arm.theta
		    print("shoulder: ", self.shoulder, " elbow: ", self.elbow, " arm: ", self.arm)

		    t = t + delta_t
		    self.display()

		#self.shoulder, self.elbow, self.arm = self.fl.follow_target_2d(self.shoulder, self.elbow, self.arm, current_target_x, current_target_y)
		#print("Al giro {}, current_target_x vale: {}, current_target_y vale: {}, current_target_z vale: {}, gli angoli sono: shoulder {}, elbow {}, arm {}".format(i, current_target_x, current_target_y, current_target_z, self.shoulder, self.elbow, self.arm))
		#sleep(deltaT)

		# TODO: Implementare correttamente il controllore posizione velocità con target finale i tre angoli.
		# TODO: Capire perchè la parte finale del braccio non ruota correttamente. (Probabilmente è dovuto al fatto che tutte le misure passategli sono relative alla parte centrale
				# e non assolute.
		# TODO: Fare in modo che il ttarget quando disegnato sulla scena non sia collegato ai movimenti della parte finale del braccio, attenzionare queste  due chiamate in quanto probabilmente causa del problema:
			# glMatrixMode(GL_MODELVIEW)
			# glMatrixMode (GL_PROJECTION)

if __name__ == '__main__':
	app = SimpleRobotArm()
	app.run()