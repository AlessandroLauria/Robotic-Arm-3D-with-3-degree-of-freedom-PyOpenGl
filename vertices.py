vertices_1 = (
	(-1, -1, 1), 
	(1, -1, 1), 
	(-1, 3, 1), 
	(1, 3, 1), 
	(-1, -1, -1), 
	(1, -1, -1), 
	(-1, 3, -1), 
	(1, 3, -1) 
	)

vertices_2 = (
	vertices_1[2], 
	vertices_1[3], 
	(3, 5, 1), 
	(5, 5, 1), 
	vertices_1[6], 
	vertices_1[7], 
	(3, 5, -1), 
	(5, 5, -1) 
	)

vertices_3 = ( 
	vertices_2[2],
	vertices_2[3],
	(7, 7, 1), 
	(9, 7, 1), 
	vertices_2[6],
	vertices_2[7],
	(7, 7, -1), 
	(9, 7, -1)
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