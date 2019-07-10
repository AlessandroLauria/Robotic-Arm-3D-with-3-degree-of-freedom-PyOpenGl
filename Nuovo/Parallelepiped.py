from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def Parallelepiped(vertices):
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vertices[vertex])
	glEnd()


vertices_base = (
	(-1, -1, 1), 
	(1, -1, 1), 
	(-1, 3, 1), 
	(1, 3, 1), 
	(-1, -1, -1), 
	(1, -1, -1), 
	(-1, 3, -1), 
	(1, 3, -1) 
	)

vertices_1 = (
	vertices_base[2],
	vertices_base[3],
	(-1, 7, 1), 
	(1, 7, 1), 
	vertices_base[6],
	vertices_base[7],
	(-1, 7, -1), 
	(1, 7, -1) 
	)

vertices_2 = (
	vertices_1[2],
	vertices_1[3],
	(-1, 11, 1), 
	(1, 11, 1), 
	vertices_1[6],
	vertices_1[7],
	(-1, 11, -1), 
	(1, 11, -1)
	)

vertices_3 = (
	vertices_2[2],
	vertices_2[3],
	(-1, 15, 1),
	(1, 15, 1),
	vertices_2[6],
	vertices_2[7],
	(-1, 15, -1),
	(1, 15, -1)
	)

vertices_target = (
	(-1, -1, 1),
	(1, -1, 1),
	(-1, 3, 1),
	(1, 3, 1),
	(-1, -1, -1),
	(1, -1, -1),
	(-1, 3, -1),
	(1, 3, -1)
)

edges = (
	(0,1),
	(0,2),
	(0,4),
	(1,3),
	(1,5),
	(4,6),
	(4,5),
	(5,7),
	(2,3),
	(2,6),
	(7,3),
	(7,6)
	)