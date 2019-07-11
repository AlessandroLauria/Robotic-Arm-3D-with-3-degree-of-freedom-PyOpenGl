# coding=utf-8

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Parallelepiped import *
import math

from PositionController import *
from SpeedController import *
from Joint import *

from Kinematics import *
from Target import *


class RobotArm:

	def __init__(self, target, kinematics):
		self.name = "Simple Robot Arm"
		self.shoulder = 90.0
		self.elbow = 0.0
		self.arm = 0.0
		self.base = 0
		self.target = target
		self.kinematics = kinematics

	def run(self):
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

		glutInitWindowSize(1000,1000)
		glutInitWindowPosition(100,100)
		glutCreateWindow(self.name)

		glClearColor(0.0, 0.0, 0.0, 0.0)
		glShadeModel(GL_FLAT)

		glutDisplayFunc(self.display)
		glutReshapeFunc(self.reshape)
		glutKeyboardFunc(self.keys)

		glutMainLoop()

	def display(self):

		glClear(GL_COLOR_BUFFER_BIT)
		glPushMatrix()
		glRotatef(self.base, 0, 1, 0)
		glPushMatrix()
		glScalef(1.0, 0.2, 0.5)
		glColor3ub(0, 255, 255)
		Parallelepiped(vertices_base)
		glPopMatrix()

		# y verso l'alto. z esce dallo schermo x classico
		glTranslatef(0, 0.60, 0)
		glRotatef(self.shoulder, 0, 0, 1)
		glTranslatef(1, -1, 0)
		glPushMatrix()
		glScalef(1.0, 0.2, 0.5)
		Parallelepiped(vertices_1)
		glPopMatrix()

		glTranslatef(1.0, 1, 0.0)
		glRotatef(self.elbow, 0.0, 0.0, 1)
		glTranslatef(1.0, -1.8, 0.0)
		glPushMatrix()
		glScalef(1.0, 0.2, 0.5)
		Parallelepiped(vertices_2)
		glPopMatrix()


		glTranslatef(1, 1.8, 0.0)
		glRotatef(self.arm, 0.0, 0.0, 1.0)
		glTranslatef(1.0, -2.6, 0.0)
		glPushMatrix()
		glScalef(1.0, 0.2, 0.5)
		Parallelepiped(vertices_3)
		glPopMatrix()
		glPopMatrix()

		glPushMatrix()
		glTranslatef(self.target.x, self.target.y, self.target.z)
		glScalef(1.0, 0.2, 0.5)
		glColor3ub(0, 255, 0);
		Parallelepiped(vertices_target)
		glPopMatrix()
		glutSwapBuffers()


	def keys(self, *args):
		key = args[0]
		if (key == b'z'):
			self.shoulder = (self.shoulder+5) % 360
		elif (key==b'x'):
			self.shoulder = (self.shoulder-5) % 360
		elif (key==b'c'):
			self.base = (self.base+5) % 360
		elif (key==b'v'):
			self.base = (self.base-5) % 360
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
		elif (key == b'p'):
			self.shoulder = 90.0
			self.elbow = 0.0
			self.arm = 0.0
		elif (key == b't'):
			self.reach_target()
		glutPostRedisplay()

	def reshape(self, w, h):
		glViewport (0, 0, w, h)
		glMatrixMode (GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(65.0, w/h, 1.0, 20.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslatef (0.0, 0.0, -16.0)


	def reach_target(self):
		#Local variable.
		delta_t = 1e-1 # 1 ms
		t = 0.0

		joint_1 = Joint(6.0, 4.0, 90)
		joint_2 = Joint(6.0, 4.0, 0)
		joint_3 = Joint(6.0, 4.0, 0)
		joint_base = Joint(6.0, 4.0, 0)

		speed_controller_1 = SpeedController(10000, 20000, 100, 100)
		speed_controller_2 = SpeedController(10000, 20000, 100, 100)
		speed_controller_3 = SpeedController(10000, 20000, 100, 100)
		speed_controller_base = SpeedController(10000, 20000, 100, 100)

		position_controller_1 = PositionController(40, 10, 10)
		position_controller_2 = PositionController(40, 10, 10)
		position_controller_3 = PositionController(40, 10, 10)
		position_controller_base = PositionController(40, 10, 10)

		#x, y, alpha = self.conversion.direct_kinematics(90, 0, 0)
		#print("Punto-->", x, y, alpha)

		theta_z = self.kinematics.compute_theta_z(self.target.x, self.target.z)

		if(self.target.z < 0 and self.target.x > 0):
			theta_z = theta_z
		elif (self.target.z > 0 and self.target.x < 0):
			theta_z = 180 - theta_z
		elif (self.target.z < 0 and self.target.x < 0):
			theta_z  = theta_z - 180
		else: #entrambi positivi
			theta_z = -theta_z

		print("Angolo di rotazione è: ", theta_z)
		#theta_z = -90
		while t < 50:
			w_target_base = position_controller_base.evaluate(theta_z, joint_base.theta, delta_t)
			output_z = speed_controller_base.evaluate(w_target_base, joint_base.w, delta_t)
			joint_base.evaluate(output_z, delta_t)
			t = t + delta_t
			self.base = joint_base.theta
			self.display()

		t = 0

		if(self.target.x <= 0):
			self.target.alpha = 3.14
		if self.target.x > 0:
			th_target_1, th_target_2, th_target_3 = self.kinematics.inverse_kinematics(self.target.x-2, self.target.y, self.target.alpha)
		else:
			th_target_1, th_target_2, th_target_3 = self.kinematics.inverse_kinematics(self.target.x+2, self.target.y, self.target.alpha)

		if self.target.x < 0 and self.target.y < 0:
		 	th_target_1 = 360 + th_target_1

		if(self.target.x <= 0 and self.target.y < 0):
			th_target_3 = -360 + th_target_3

		print("Th1-->", th_target_1,"Th2-->", th_target_2,"Th3-->", th_target_3)
		while t < 50:
			#Position controller
			w_target_1 = position_controller_1.evaluate(th_target_1, joint_1.theta, delta_t)
			w_target_2 = position_controller_2.evaluate(th_target_2, joint_2.theta, delta_t)
			w_target_3 = position_controller_3.evaluate(th_target_3, joint_3.theta, delta_t)
			#Speed controller
			output_1 = speed_controller_1.evaluate(w_target_1, joint_1.w, delta_t)
			output_2 = speed_controller_2.evaluate(w_target_2, joint_2.w, delta_t)
			output_3 = speed_controller_3.evaluate(w_target_3, joint_3.w, delta_t)
			#Update joint value
			joint_1.evaluate(output_1, delta_t)
			joint_2.evaluate(output_2, delta_t)
			joint_3.evaluate(output_3, delta_t)
			#Update scenes.
			self.shoulder = joint_1.theta
			self.elbow = joint_2.theta
			self.arm = joint_3.theta
			self.display()
			#Increment t.
			t = t + delta_t
		x, y, alpha = self.kinematics.direct_kinematics(self.shoulder, self.elbow, self.arm)

		#x, y, alpha = self.conversion.direct_kinematics(joint_1.theta, joint_2.theta, joint_3.theta)
		print("X-->", x, ", Y-->", y, ", alpha-->", alpha)
		#print("I target valgono:", target.x, target.y, target.z)

