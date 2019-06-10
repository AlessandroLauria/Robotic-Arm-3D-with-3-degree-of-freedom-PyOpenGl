from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from vertices import *
from reach_target import *
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

		print("Display")
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
		glRotatef(self.arm, 0.0, 1.0, 1.0)
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
			print(self.arm)
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
		#Start target (current position)
		current_target_x = 0
		current_target_y = 0
		current_target_z = 0
		deltaT = 0.00001
		i = 0
		finalShoulder, finalElbow, finalArm = self.fl.reach_target_2d(self.shoulder, self.elbow, self.arm, target_x_final, target_y_final)
		finalShoulder = round(finalShoulder, 1)
		finalElbow = round(finalElbow, 1)
		finalArm = round(finalArm, 1)

		if self.shoulder < finalShoulder:
			self.shoulder += 0.1
		elif self.shoulder > finalShoulder:
			self.shoulder -= 0.1
		if self.elbow < finalElbow:
			self.elbow += 0.1
		elif self.elbow > finalElbow:
			self.elbow -= 0.1
		if self.arm < finalArm:
			self.arm += 0.1
		elif self.arm > finalArm:
			self.arm -= 0.1

		#self.shoulder, self.elbow, self.arm = self.fl.follow_target_2d(self.shoulder, self.elbow, self.arm, current_target_x, current_target_y)
		i += 1
		#print("Al giro {}, current_target_x vale: {}, current_target_y vale: {}, current_target_z vale: {}, gli angoli sono: shoulder {}, elbow {}, arm {}".format(i, current_target_x, current_target_y, current_target_z, self.shoulder, self.elbow, self.arm))
		self.display()
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