def trilaterate(data,last_place,index):
# import data, each needs to be list format
	x, y, z, r = data
	p = last_place
	i = index
	new_x, new_y, new_z, new_r = x[p:i+1], y[p:i+1], z[p:i+1], r[p:i+1] # we look only at the new secion of data
	d1 = []
	d2 = []
	d3 = []
	d4 = []
	xsums = []
	ysums = []
	zsums = []
	
# pick four points equidistant in time along current data set
	start = 0
	c = int((len(new_x)-1)/3)
	d1.extend([new_x[start],new_y[start],new_z[start],new_r[start]])
	d2.extend([new_x[c],new_y[c],new_z[c],new_r[c]])
	d3.extend([new_x[2*c],new_y[2*c],new_z[2*c],new_r[2*c]])
	d4.extend([new_x[3*c],new_y[3*c],new_z[3*c],new_r[3*c]])			

# Trilateration calculation, using Cramers Rule to solve. System of 4 equations created by the 4 input points and the 4 input distances.
# The two arrays from reduced system of 3 equations
	A=[[2*(d2[0]-d1[0]),2*(d2[1]-d1[1]),2*(d2[2]-d1[2])],[2*(d3[0]-d1[0]),2*(d3[1]-d1[1]),2*(d3[2]-d1[2])],[2*(d4[0]-d1[0]),2*(d4[1]-d1[1]),2*(d4[2]-d1[2])]]
	B=[(d1[3]**2-d2[3]**2)-(d1[0]**2-d2[0]**2)-(d1[1]**2-d2[1]**2)-(d1[2]**2-d2[2]**2),(d1[3]**2-d3[3]**2)-(d1[0]**2-d3[0]**2)-(d1[1]**2-d3[1]**2)-(d1[2]**2-d3[2]**2),(d1[3]**2-d4[3]**2)-(d1[0]**2-d4[0]**2)-(d1[1]**2-d4[1]**2)-(d1[2]**2-d4[2]**2)]
	C=[[2*(d2[0]-d1[0]),2*(d2[1]-d1[1]),2*(d2[2]-d1[2])],[2*(d3[0]-d1[0]),2*(d3[1]-d1[1]),2*(d3[2]-d1[2])],[2*(d4[0]-d1[0]),2*(d4[1]-d1[1]),2*(d4[2]-d1[2])]]
	X=[]

# Cramer's Rule
	import numpy as np
	from numpy import linalg
	det = linalg.det(A)
	if det != 0:
		for i in range(0,len(B)):
			for j in range(0,len(B)):
				C[j][i]=B[j]
				if i>0:
					C[j][i-1]=A[j][i-1]
			X.append(linalg.det(C)/linalg.det(A)) 
		return( 
			[X[0],X[1],X[2],d1,d2,d3,d4]
			)
	else:
		return (
			["Determinant of A = 0, Singular Matrix \nHere are the chosen points: \nP1: %r \nP2: %r \nP3: %r \nP4: %r" % (d1,d2,d3,d4)]
			)
		
		
def least_squares(data,last_place,index):
# import data, each needs to be list format
	x, y, z, r = data
	p = last_place
	lp = p
	i = index
	x_list = x
	y_list = y
	z_list = z
	r_list = r
# use any random coordinate in (x,y,z,r) as initial guess
	initial_guess = (4,5,6,7)
# create least squares equations and save them to an equations.py file
	text_file = open("equations.py", "w")
	text_file.write("def equations( guess):\n")
	text_file.write("\tx, y, z, r = guess\n\n")
	text_file.write("\treturn (\n")

	while p <= i:
		text_file.write("\t\t(x - {})**2 + (y - {})**2 + (z - {})**2 - (r -{})**2,\n".format(x_list[p], y_list[p], z_list[p], r_list[p]))
		p=p+1
	text_file.write("\t)")    
	text_file.close()
# make SciPy solve the system using an initial guess.
	from equations import equations
	import scipy
	from scipy.optimize import least_squares
	results = least_squares(equations, initial_guess)
# print out solution
	return (
		[results.x[0],results.x[1],results.x[2],x_list[lp:i+1],y_list[lp:i+1],z_list[lp:i+1]]
	)
