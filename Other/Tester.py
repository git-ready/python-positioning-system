# -*- coding: utf-8 -*-
# Plots a flight (circle) and the location of the slave
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib.pyplot import show, plot
from matplotlib import style
import math
import numpy as np
from numpy import linalg
import scipy
from scipy.optimize import least_squares

red = '#fd9696'
yellow = '#fde396'
blue = '#96cafd'


style.use('ggplot')
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

x = []
y = []
z = []
# Slave coordinates – when trilat or least squares is processed the result should be close to this 
Xs=5
Ys=5
Zs=1
# Flight path – the set of coordinates processed with trilat or least squares
x_center = 50
y_center = 40
z_center = 10
points = 45
radius = 25
slice = 2 * math.pi/points

# Generate the x,y,z coordinates
for i in range(0, points):
    angle = slice * i
    x.append(x_center + radius * math.cos(angle))
    y.append(y_center + radius * math.sin (angle))
    z.append(z_center-.05*i)

# Generate the scatter plots for the flight path and the slave location
ax1.scatter(x, y, z, color=red, marker='o')
ax1.scatter(Xs, Ys, Zs, color=blue, marker='o')
ax1.set_xlabel('x axis')
ax1.set_ylabel('y axis')
ax1.set_zlabel('z axis')
ax1.set_title('Flight Coordinates & Slave Location')
ax1.text(Xs,Ys,Zs, '"Unkown" Slave Location: %r'%[Xs,Ys,Zs], color=blue)

# Save off the x,y,z, and generate the range to slave
myFile = open("flight.csv", "w")
myFile.write("{},{},{},{}\n".format("X", "Y", "Z", "Range"))
r = []
for num in range(0, points):
	sRange = math.sqrt(math.pow((x[num]- Xs),2)+ math.pow((y[num]- Ys),2)+ math.pow((z[num]- Zs),2))
	r.append(sRange)
	myFile.write("{},{},{},{}\n".format(x[num], y[num], z[num], sRange))
	
myFile.close()
# Generate the plot
plt.show(block=False)
# -----------------------------------------------------------------------------------------------------------------------------------------
# Find Slave Coordinates using four points from fligh path and the four ranges.
# -----------------------------------------------------------------------------------------------------------------------------------------
print "\n\nBasic 4-Point Trilateration Press 1 -------------- Least Squares Trilateration Press 2\n"
go = raw_input(">>> ")
if go == '1':
# Finding 4 points in flight path far away from eachother
	p1 = []
	p2 = []
	p3 = []
	p4 = []
	xsums = []
	ysums = []
	zsums = []
	print("\nPick a Point in Time on Flight Path\nEnter Integers Only Between 0 and %r.\n") % points
	start = int(raw_input(">>> "))
	p1.extend([x[start],y[start],z[start]])
# Scan flight path for max distance from the starting point along x, y and z
	for i in range(0,points):
		xsums.append( x[start] - x[i] )
		ysums.append( y[start] - y[i] )
		zsums.append( z[start] - z[i] )
	xm = max(xsums)
	ym = max(ysums)
	zm = max(zsums) 
	print "\nXmax = %r\nYmax = %r\nZmax = %r\n" % (xm, ym, zm)
# Find the max distance indexes, pick the points
	for i in range(0,points):
		if xsums[i] == xm:
			p2.extend([x[i],y[i],z[i]])
			print "Max X Index: %i" % i
	for i in range(0,points):
		if ysums[i] == ym:
			p3.extend([x[i],y[i],z[i]])
			print "Max Y Index: %i" % i
	for i in range(0,points):
		if zsums[i] == zm:
			p4.extend([x[i],y[i],z[i]])	
			print "Max Z Index: %i" % i

# "PTP Timestamp Data" distances from each point to the slave
	d1 = math.sqrt(math.pow((p1[0]- Xs),2)+ math.pow((p1[1]- Ys),2)+ math.pow((p1[2]- Zs),2))
	d2 = math.sqrt(math.pow((p2[0]- Xs),2)+ math.pow((p2[1]- Ys),2)+ math.pow((p2[2]- Zs),2))
	d3 = math.sqrt(math.pow((p3[0]- Xs),2)+ math.pow((p3[1]- Ys),2)+ math.pow((p3[2]- Zs),2))
	d4 = math.sqrt(math.pow((p4[0]- Xs),2)+ math.pow((p4[1]- Ys),2)+ math.pow((p4[2]- Zs),2))
	
# Round for display only			
	p1r = [round(elem, 1) for elem in p1]
	p2r = [round(elem, 1) for elem in p2]
	p3r = [round(elem, 1) for elem in p3]
	p4r = [round(elem, 1) for elem in p4]
	d1r = round(d1, 1)
	d2r = round(d2, 1)
	d3r = round(d3, 1)
	d4r = round(d4, 1)

# Trilateration calculation, using Cramers Rule to solve, system of 4 equations created by the 4 input points and the 4 input distances.
	print("\nInputs for Algorithm (Cramer's Rule)\nPoint 1:%s, Dist 1: %s\nPoint 2:%s, Dist 2: %s\nPoint 3:%s, Dist 3: %s\nPoint 4:%s, Dist 4: %s\n") % (p1r,d1r,p2r,d2r,p3r,d3r,p4r,d4r)
# Generate plot showing chosen points
	fig2 = plt.figure()
	ax2 = fig2.add_subplot(111, projection='3d')
	ax2.set_xlabel('x axis')
	ax2.set_ylabel('y axis')
	ax2.set_zlabel('z axis')
	ax2.scatter( [p1[0],p2[0],p3[0],p4[0]], [p1[1],p2[1],p3[1],p4[1]], [p1[2],p2[2],p3[2],p4[2]], color=red)
	ax2.text(p1r[0]-20,p1r[1]+10,p1r[2], '%r'%[p1r[0],p1r[1],p1r[2]], color=blue, zdir='y')
	ax2.text(p2r[0]-20,p2r[1]+10,p2r[2], '%r'%[p2r[0],p2r[1],p2r[2]], color=blue, zdir='y')
	ax2.text(p3r[0]-20,p3r[1]+10,p3r[2], '%r'%[p3r[0],p3r[1],p3r[2]], color=blue, zdir='y')
	ax2.text(p4r[0]-20,p4r[1]+10,p4r[2], '%r'%[p4r[0],p4r[1],p4r[2]], color=blue, zdir='y')
	ax2.set_title('Trilateration Points')
	plt.show(block=False)
# The two arrays from reduced system of 3 equations
	A=[[2*(p2[0]-p1[0]),2*(p2[1]-p1[1]),2*(p2[2]-p1[2])],[2*(p3[0]-p1[0]),2*(p3[1]-p1[1]),2*(p3[2]-p1[2])],[2*(p4[0]-p1[0]),2*(p4[1]-p1[1]),2*(p4[2]-p1[2])]]
	B=[(d1**2-d2**2)-(p1[0]**2-p2[0]**2)-(p1[1]**2-p2[1]**2)-(p1[2]**2-p2[2]**2),(d1**2-d3**2)-(p1[0]**2-p3[0]**2)-(p1[1]**2-p3[1]**2)-(p1[2]**2-p3[2]**2),(d1**2-d4**2)-(p1[0]**2-p4[0]**2)-(p1[1]**2-p4[1]**2)-(p1[2]**2-p4[2]**2)]
	C=[[2*(p2[0]-p1[0]),2*(p2[1]-p1[1]),2*(p2[2]-p1[2])],[2*(p3[0]-p1[0]),2*(p3[1]-p1[1]),2*(p3[2]-p1[2])],[2*(p4[0]-p1[0]),2*(p4[1]-p1[1]),2*(p4[2]-p1[2])]]
	X=[]
# Cramer's Rule
	det = linalg.det(A)
	if det != 0:
		if raw_input("\nCalculate Press 1\n>>> ") == '1':
			for i in range(0,len(B)):
				for j in range(0,len(B)):
					C[j][i]=B[j]
					if i>0:
						C[j][i-1]=A[j][i-1]
				X.append(round(linalg.det(C)/linalg.det(A),3)) 
		print('\n\n>>>> x=%s, y=%s, z=%s <<<<\n') % (X[0],X[1],X[2])
		
		
		
		fig3 = plt.figure()
		ax3 = fig3.add_subplot(111, projection='3d')
		ax3.set_xlabel('x axis')
		ax3.set_ylabel('y axis')
		ax3.set_zlabel('z axis')
		ax3.scatter( [p1[0],p2[0],p3[0],p4[0]], [p1[1],p2[1],p3[1],p4[1]], [p1[2],p2[2],p3[2],p4[2]], color=red)
		ax3.plot([p1[0],X[0]],[p1[1],X[1]],[p1[2],X[2]], color=yellow) # connect the points by a line
		ax3.plot([p2[0],X[0]],[p2[1],X[1]],[p2[2],X[2]], color=yellow)
		ax3.plot([p3[0],X[0]],[p3[1],X[1]],[p3[2],X[2]], color=yellow)
		ax3.plot([p4[0],X[0]],[p4[1],X[1]],[p4[2],X[2]], color=yellow)
		slv = [X[0],X[1],X[2]]
		ax3.text(X[0],X[1],X[2], 'Output: %r'%slv, color=blue)
		ax3.scatter( X[0],X[1],X[2], c=blue)
		ax3.set_title('Trilateration Output')
		plt.show(block=False)
		raw_input()
	else: 
		print("Determinant of A = 0, Singular Matrix, No Solution")

# -----------------------------------------------------------------------------------------------------------------------------------------
# Find Slave Coordinates Using Least Squares 
# -----------------------------------------------------------------------------------------------------------------------------------------
elif go == '2':
	x_list = x
	y_list = y
	z_list = z
	r_list = r
	print"\nSolve With Initial Guess:\n"
	Xi = int(raw_input(">>> Xi = "))
	Yi = int(raw_input(">>> Yi = "))
	Zi = int(raw_input(">>> Zi = "))
	initial_guess = (Xi,Yi,Zi,0)
	print"\nUsing (%r, %r, %r) as initial guess, Press Enter\n>>>" % (Xi, Yi, Zi)
	raw_input()
# Creating the Least Squares Equations, saving them to an equations.py file
	text_file = open("equations.py", "w")
	text_file.write("def equations( guess):\n")
	text_file.write("\tx, y, z, r = guess\n\n")
	text_file.write("\treturn (\n")

	i=0

	while i < len(x)-1:
		text_file.write("\t\t(x - {})**2 + (y - {})**2 + (z - {})**2 - (r -{})**2,\n".format(x_list[i], y_list[i], z_list[i], r_list[i]))
		i=i+1
	text_file.write("\t)")    
    
	text_file.close()
# make SciPy solve the system using an initial guess.
	from equations import equations
	results = least_squares(equations, initial_guess)
# print out solution
	output_pt = [results.x[0],results.x[1],results.x[2]]
	out_disp = [round(results.x[0],6),round(results.x[1],6),round(results.x[2],6)]
	print "\nLeast Squares Output: %r" % output_pt
# print out 3d plot	
	fig4 = plt.figure()
	ax4 = fig4.add_subplot(111, projection='3d')
	ax4.set_xlabel('x axis')
	ax4.set_ylabel('y axis')
	ax4.set_zlabel('z axis')
# flight path
	ax4.scatter(x, y, z, c=red, marker='o',alpha=0.75) 
# connect the dots
	for i in range(0,points):
		ax4.plot([x[i],results.x[0]],[y[i],results.x[1]],[z[i],results.x[2]],color=yellow,alpha=.95)
# slave location
	ax4.scatter(results.x[0],results.x[1],results.x[2], color=blue)
	ax4.text(results.x[0]+7,results.x[1]-7,results.x[2], "Output: %r"%out_disp, color=blue)
	ax4.set_title('Least Squares Output')
	plt.show(block=False)
	raw_input()
	
	
	
	