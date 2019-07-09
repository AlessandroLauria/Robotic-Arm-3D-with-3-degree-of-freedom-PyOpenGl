
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class SimpleRobotArm:

    def __init__(self):
        self.name= "Simple Robot Arm"
        self.shoulder = 90.0
        self.elbow = 0.0
        self.arm = 0.0
        self.wrist = 0.0
        self.finger1= 0.0
        self.finger2= 0.0
        self.finger3= 0.0


    def run(self):

        glutInit(sys.argv) # initialise the system
        # Configure inital display mode
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

        # Set up and display initial window
        glutInitWindowSize(1000,1000)
        glutInitWindowPosition(100,100)
        glutCreateWindow(self.name)  # See the __init__ method for self.name

        # Initial colour and shading model
        glClearColor(0.0,0.0,0.0,0.0)
        glShadeModel(GL_FLAT)

        # Register callback methods. The arguments are the names of
        # methods defined below.
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        # glutMouseFunc(self.mouse) # not needed here
        glutKeyboardFunc(self.keys)

        # Launch the OGL event processing loop
        glutMainLoop()

    def display(self):
        glClear (GL_COLOR_BUFFER_BIT);
        glPushMatrix();
        glTranslatef (-4.0, -3.0, -3.0);
        glRotatef (self.shoulder, 0.0, 0.0, 1.0);
        glTranslatef (1.0, 0.0, 0.0);
        glPushMatrix();
        glScalef (2.0, 0.2, 0.5);
        glutWireCube (1.0);
        glPopMatrix();

        glTranslatef (1.0, 0.0, 0.0);
        glRotatef (self.elbow, 0.0, 0.0, 0.8);
        glTranslatef (1.0, 0.0, 0.0);
        glPushMatrix();
        glScalef (2.0, 0.2, 0.5);
        glutWireCube (1.0);
        glPopMatrix();

        glTranslatef (1.0, 0.0, 0.0);
        glRotatef (self.arm, 0.0, 1.0, 1.0);
        glTranslatef (1.0, 0.0, 0.0);
        glPushMatrix();
        glScalef (2.0, 0.2, 0.5);
        glutWireCube (1.0);
        glPopMatrix();


        glTranslatef (1.0, 0.0, 0.0);
        glRotatef (self.wrist, 0.0, 0.0, 0.0);
        glTranslatef (0.3, 0.0, 0.0);
        glPushMatrix();
        glScalef (0.6, 0.7, 0.8);
        glutWireCube (1.0);
        glPopMatrix();


        glTranslatef (0.0, 0.3, 0.2);
        glRotatef (self.finger1, 0.0, 0.0, 1.0);
        glTranslatef (1.0, 0.0, 0.0);
        glPushMatrix();
        glScalef (1.5, 0.1, 0.1);
        glutWireCube (1.0);
        glPopMatrix();

        glTranslatef (0.0, 0.0, -0.5);
        glRotatef (self.finger2, 0.0, 0.0, 1.0);
        glTranslatef (0.0,0.0,0.0);
        glPushMatrix();
        glScalef (1.5, 0.1, 0.1);
        glutWireCube (1.0);
        glPopMatrix();


        glTranslatef(0.0,-0.6,0.3)
        glRotatef (self.finger3, 0.0, 0.0, 1.0);
        glTranslatef (0.0,0.0,0.0);
        glPushMatrix();
        glScalef (1.5, 0.1, 0.1);
        glutWireCube (1.0);
        glPopMatrix();

        glPopMatrix();
        glutSwapBuffers();

    def reshape(self,w,h):
        glViewport (0, 0, w, h)
        glMatrixMode (GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, w/h, 1.0, 20.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef (0.0, 0.0, -6.0)

    def keys(self,*args):
        key = args[0]
        if (key == 's'):
            self.shoulder = (self.shoulder+5) % 360
        elif (key=='S'):
            self.shoulder = (self.shoulder-5) % 360
        elif (key=='e'):
            self.elbow = (self.elbow+5) % 360
        elif (key=='E'):
            self.elbow = (self.elbow-5) % 360
        elif (key=='w'):
            self.arm = (self.arm+5) % 360
        elif (key=='W'):
            self.arm = (self.arm-5) % 360
        elif (key=='q'):
            self.finger1 = (self.finger1-5) % 360
        elif (key=='Q'):
            self.finger1 = (self.finger1+5) % 360
        elif (key=='a'):
            self.finger2 = (self.finger2-5) % 360
        elif (key=='A'):
            self.finger2 = (self.finger2+5) % 360
        elif (key=='x'):
            self.finger3 = (self.finger3-5) % 360
        elif (key=='X'):
            self.finger3 = (self.finger3+5) % 360


        glutPostRedisplay()

if __name__ == '__main__':
    app = SimpleRobotArm()
    app.run()
