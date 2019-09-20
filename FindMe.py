# -*- coding: utf-8 -*- 
from matplotlib import pyplot, style
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import show, plot
import math
import time
import random
from Find_Me_Functions import trilaterate
from Find_Me_Functions import least_squares

gblue = '#4285f4'
gyellow = '#fbbc05'
ggreen = '#34a853'
gred = '#ea4335'

# initiate plots
style.use('ggplot')

#fig1 = pyplot.figure(num='Algebraic Solution', figsize=[7,7], dpi=100, clear=False)
#sub1 = fig1.add_subplot(1, 1, 1, projection='3d')
#sub1.set_title('Four Point Lateration', alpha=0.5, fontsize=15)
#sub1.set_xlabel('Latitude (meters)', alpha=0.5, fontsize=10)
#sub1.set_ylabel('Longitude (meters)', alpha=0.5, fontsize=10)
#sub1.set_zlabel('Altitude (meters)', alpha=0.5, fontsize=10)

fig2 = pyplot.figure(num='Regression Solution', figsize=[6,6], dpi=100, clear=False)
sub2 = fig2.add_subplot(1, 1, 1, projection='3d')
sub2.set_title('Least Squares Lateration', alpha=0.5, fontsize=15)
sub2.set_xlabel('Latitude (meters)', alpha=0.5, fontsize=10)
sub2.set_ylabel('Longitude (meters)', alpha=0.5, fontsize=10)
sub2.set_zlabel('Altitude (meters)', alpha=0.5, fontsize=10)

fig4 = pyplot.figure(num='Range Data', figsize=[7,7], dpi=100, clear=False)
sub4 = fig4.add_subplot(1, 1, 1)

pyplot.ion()
fig3 = pyplot.figure(num='Simulation', figsize=[6,6], dpi=100, clear=False)
sub3 = fig3.add_subplot(1, 1, 1, projection='3d')

# -------------------------------------- CREATE FLIGHT PATH ------------------------------------------
lat, lon, alt = [], [], []
# Pick a flight path reference point and slave location on the earth
init_lat = 40.495715
init_lon = -80.245828
init_alt = 700 # meters above sea level
slv_lat = 40.133509
slv_lon = -79.989699
slv_alt = 0 # meters above ground level

x_center = init_lat
y_center = init_lon
points = 120 # points in flight
radius = 6000 # meters
slice = 2 * math.pi/points

# Generate latitude longitude, altidude for Google Earth flight path
for i in range(0, points):
	angle = slice * i
	lat.append(x_center + radius * math.cos(angle)*0.00001) # 0.00001 degrees per meter
	lon.append(y_center + 2*radius * math.sin(angle)*0.00001)
	alt.append(init_alt)
	init_alt = init_alt+4.0

# Convert latitude longitude altitudes to meters for calculations
x, y, z, r = [], [], [], []
# define slave as origin
Xs=0
Ys=0
Zs=0
times = []
rn = []
fluctuation = 5 #meters
for i in range(0,points):
	noise = random.random()
	x.append( (lat[i]-slv_lat)*100000.0 ) # 100000 meters per degree
	y.append( (lon[i]-slv_lon)*100000.0 )
	z.append( alt[i]-slv_alt )
	sRange = math.sqrt(math.pow((x[i]- Xs),2)+ math.pow((y[i]- Ys),2)+ math.pow((z[i]- Zs),2))
	r.append(sRange)
	if i % 2 == 0: #even
		rn.append(sRange + fluctuation*noise)
	else: #odd
		rn.append(sRange - fluctuation*noise)
	times.append(i)


# plot the noise

sub4.set_title('Range Data vs. Time', alpha=0.5, fontsize=15)
sub4.set_xlabel('Time', alpha=0.5, fontsize=10)
sub4.set_ylabel('Range (meters)', alpha=0.5, fontsize=10)
sub4.scatter(times, r, color=gblue, s=25, marker='x', label='Exact Range Data')
sub4.scatter(times, rn, color=gred, s=15, marker='o', label='Noisy Range Data: +/- %s meters'% fluctuation)
sub4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07), shadow=True, ncol=2)

# plot the path
sub3.set_title('Planned Flight Path', alpha=0.5, fontsize=15)
sub3.set_xlabel('Latitude (meters)', alpha=0.5, fontsize=10)
sub3.set_ylabel('Longitude (meters)', alpha=0.5, fontsize=10)
sub3.set_zlabel('Altitude (meters)', alpha=0.5, fontsize=10)
sub3.scatter(x, y, z, color=gblue, s=25, marker='o', label='Planned Flight Path')
sub3.scatter(Xs,Ys,Zs, color=gred, s = 50, marker='v', label='Actual Position')
sub3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)
sub3.text(x[0], y[0], z[0], 'Start', alpha=0.5, fontsize=10)
sub3.text(x[points-1], y[points-1], z[points-1], 'Stop', alpha=0.5, fontsize=10)

# -------------------------------------- GENERATE KML FILE ------------------------------------------
coordinates = []
for i in range(0,points):
	string = '%r,%r,%r\n              ' % (lon[i],lat[i],alt[i])
	coordinates.append(string)

kml_coordinates = ''.join(coordinates)	
kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>Absolute Extruded.kml</name>
	<StyleMap id="yellowLineGreenPoly">
		<Pair>
			<key>normal</key>
			<styleUrl>#yellowLineGreenPoly1</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#yellowLineGreenPoly0</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="yellowLineGreenPoly0">
		<LineStyle>
			<color>7f0ef777</color>
			<width>1.5</width>
		</LineStyle>
		<PolyStyle>
			<color>b3aa7f19</color>
		</PolyStyle>
	</Style>
	<Style id="yellowLineGreenPoly1">
		<LineStyle>
			<color>7f0ef777</color>
			<width>1.5</width>
		</LineStyle>
		<PolyStyle>
			<color>b3aa7f19</color>
		</PolyStyle>
	</Style>
	<Placemark>
		<name>Absolute Extruded</name>
		<description>Transparent green wall with yellow outlines</description>
		<styleUrl>#yellowLineGreenPoly</styleUrl>
		<LineString>
			<extrude>1</extrude>
			<tessellate>1</tessellate>
			<altitudeMode>absolute</altitudeMode>
			<coordinates>
			%s
			</coordinates>
		</LineString>
	</Placemark>
</Document>
</kml>
""" % kml_coordinates
target = open('Path.kml', 'w')
target.truncate() 
target.write(kml)
target.close()

slv_kml = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
  <Document>
	<name>Position.kml</name>
	<Style id="hl">
		<IconStyle>
			<scale>1.3</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/paddle/blu-blank.png</href>
			</Icon>
			<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<ListStyle>
			<ItemIcon>
				<href>http://maps.google.com/mapfiles/kml/paddle/blu-blank-lv.png</href>
			</ItemIcon>
		</ListStyle>
	</Style>
	<StyleMap id="default">
		<Pair>
			<key>normal</key>
			<styleUrl>#default0</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#hl</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="default0">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/paddle/blu-blank.png</href>
			</Icon>
			<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<ListStyle>
			<ItemIcon>
				<href>http://maps.google.com/mapfiles/kml/paddle/blu-blank-lv.png</href>
			</ItemIcon>
		</ListStyle>
	</Style>
	<Placemark>
		<name>Actual Position</name>
		<description>Attached to the ground. Intelligently places itself 
       at the height of the underlying terrain.</description>
		<styleUrl>#default</styleUrl>
		<Point>
			<coordinates>%s,%s,%s</coordinates>
		</Point>
	</Placemark>
</Document>
</kml>''' % (slv_lon,slv_lat,slv_alt)
target = open('Position.kml', 'w')
target.truncate() 
target.write(slv_kml)
target.close()

# -------------------------------------- BEGIN PROCESSING ------------------------------------------
raw_input('\nDisplaying Planned Flight\n>>> ')
pyplot.show(block=False)

# package up data for calculations
input = raw_input('To use Noisy Range Data (+/- %s m) PRESS 1\nTo use Exact Range Data PRESS 2\n>>> ' % fluctuation)
if int(input) == 1:
	data = [x,y,z,rn]
elif int(input) == 2:
	data = [x,y,z,r]
else:
	data = [x,y,z,r]
raw_input('Press "ENTER" To Start\n>>> ')
a, b, c, d = [], [], [], []
sxls, syls, szls, xin, yin, zin, sx, sy, sz, tx, ty, tz = [], [], [], [], [], [], [], [] ,[], [], [], []
i = 0
j = 0
p = 0
while True:
	# check if there is data
	if i < len(x):
		# feed the functions one data packet per loop
		a.append(data[0][i])
		b.append(data[1][i])
		c.append(data[2][i])
		d.append(data[3][i])
		data_feed = [a,b,c,d]
	
		# clear plots
#		sub1.cla()
		sub2.cla()
		# processing block - try for a calculation every 10 new data packets
		if j > 9:
			
			# make sure the field of view is sufficient for the calculations
			#print "a: %r\nb: %r\nc: %r\ni: %r\np: %r" % (a,b,c,i,p)
			#raw_input('')
			FltRange = math.sqrt(math.pow((a[i] - a[p]),2) + math.pow((b[i] - b[p]),2) + math.pow((c[i] - c[p]),2))
			SlvRange = d[p]
			Ratio = SlvRange/FltRange
			threshold = 6.0
			
			if Ratio < threshold:
				#---------------------------------------------------------- LEAST SQUARES BLOCK----------------------------------------------------------------
				# calculate slave position, least_squares() looks a the newest 10 packets in data feed, makes 10 equations, calculates one output
				result = least_squares(data_feed,p,i)
				# save results/inputs to lists - the s(x,y,z)ls points are the slave coordinates, the (x,y,z)in are the flight points used to calculate
				print '\n--------------------------------------Time: %s Seconds--------------------------------------' % i
				print "View Good (ratio less than %s)\nUsing %s Points" % (threshold, len(result[3])) 
				print "Predicted = %.3f deg W, %.3f deg N, %.3f m" % ( (result[1]*0.00001 + slv_lon), (result[0]*0.00001 + slv_lat), result[2] )
				print "Actual    = %.3f deg W, %.3f deg N, %.3f m" % (slv_lon,slv_lat,slv_alt)
				
				sxls.append(result[0])
				syls.append(result[1])
				szls.append(result[2])
				xin.append(result[3])
				yin.append(result[4])
				zin.append(result[5])
			
#				# ------------------------------------------------------------- TRILAT BLOCK -----------------------------------------------------------------------
#				# calculate slave position - trilaterate() looks at the newest 10 packets in data feed, chooses four of those points, calculates one output
#				result1 = trilaterate(data_feed,p,i)
#				# save results/inputs to lists - the t(x,y,z) points are the four points chosen to trilaterate, the s(x,y,z) points are the slave coordinates
#				print "Trilat = %r\n" %result1[0:3]
#				sx.append(result1[0])
#				sy.append(result1[1])
#				sz.append(result1[2])
#				tx.extend([result1[3][0],result1[4][0],result1[5][0],result1[6][0]])
#				ty.extend([result1[3][1],result1[4][1],result1[5][1],result1[6][1]])
#				tz.extend([result1[3][2],result1[4][2],result1[5][2],result1[6][2]])
				
				# capture the last value used, start the count for 10 new points
				p = i
				j = 0
				
			else:
				# start the count for 10 new points
				j = 0
				print('\nView Too Small: (Range to Target)/(Current Flight Range) = %s\nWait for more data...' % round(SlvRange/FltRange,3))
			
		i = i + 1
		j = j + 1
			
		# ------------------------------------------------------------- PLOT THE DATA -----------------------------------------------------------------------
#		sub1.set_title('Four Point Lateration', alpha=0.5, fontsize=15)
#		sub1.set_xlabel('Latitude (meters)', alpha=0.5, fontsize=10)
#		sub1.set_ylabel('Longitude (meters)', alpha=0.5, fontsize=10)
#		sub1.set_zlabel('Altitude (meters)', alpha=0.5, fontsize=10)
#		sub1.scatter(a, b, c, color=gblue, s=25, marker='o', label='Flight Path')
#		sub1.scatter(Xs, Ys, Zs, color=gred, s=25, marker='o', label='Actual Position')
#		# plot the lines (results)
#		if len(tx) != 0:
#			sub1.scatter(result1[0],result1[1],result1[2], color=ggreen, s = 50, marker='o', label='Predicted Position')
#			r = 0
#			s = 0
#			t = 0
#			colors = [gblue,gred,gyellow,ggreen]
#			for v in range(0,len(tx)):
#				if r == 4:
#					s = s + 1
#					t = t +1
#					r = 0
#					if t == 4:
#						t = 0
#				sub1.plot( [tx[v],sx[s]], [ty[v],sy[s]], [tz[v],sz[s]], color=colors[t])
#				r = r + 1
#		sub1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=3)
		
		sub2.set_title('Least Squares Lateration', alpha=0.5, fontsize=15)
		sub2.set_xlabel('Latitude (meters)', alpha=0.5, fontsize=10)
		sub2.set_ylabel('Longitude (meters)', alpha=0.5, fontsize=10)
		sub2.set_zlabel('Altitude (meters)', alpha=0.5, fontsize=10)
		sub2.scatter(a, b, c, color=gblue, s=25, marker='o', label='Flight Path')
		sub2.scatter(Xs, Ys, Zs, color=gred, s=50, marker='v', label='Actual Position')
		# plot the lines (results)
		if len(xin) != 0:
			sub2.scatter(result[0],result[1],result[2], color=ggreen, s = 50, marker='o', label='Predicted Position')
			r = 0
			s = 0
			t = 0
			colors = [gblue,gred,gyellow,ggreen]
			for next in range(0,len(xin)):
				for v in range(0,len(xin[next])):
					if r == len(xin[next])-1: # the two if statements are just to alternate the line color
						t = t + 1
						r = 0
						if t == 4:
							t = 0
					sub2.plot( [ xin[next][v],sxls[next] ], [ yin[next][v],syls[next] ], [ zin[next][v],szls[next] ], color=colors[t], alpha=0.2 )
					r = r + 1
					
		sub2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=3)
		
		pyplot.show(block=False)
		pyplot.pause(1)
		
		# --------------------------------------------------------- UPDATE GOOGLE EARTH PLOT -----------------------------------------------------------
		
	# plot flight points
		coordinates2 = []
		for value in range(0,i):
			string ='''
			<Placemark>
			<Point>
				<altitudeMode>absolute</altitudeMode>
				<coordinates>%r,%r,%r</coordinates>
			</Point>
			</Placemark>\n\n''' % (lon[value],lat[value],alt[value])
			coordinates2.append(string)

		kml_coordinates = ''.join(coordinates2)
		
		kml = """<?xml version="1.0" encoding="UTF-8"?>
		<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
			<Document>
				<name>RTPoints.kml</name>
				%s
			</Document>
		</kml>
		""" % kml_coordinates
		target = open('RT_Points.kml', 'w')
		target.truncate() 
		target.write(kml)
		target.close()
		
	# plot current position solution
		if len(xin) != 0:
			string ='''
			<Placemark>
			<name>Predicted Position</name>
			<Point>
				<altitudeMode>relativeToGround</altitudeMode>
				<coordinates>%r,%r,0</coordinates>
			</Point>
			</Placemark>\n\n''' % ( syls[-1]*0.00001+slv_lon, sxls[-1]*0.00001+slv_lat) 
		
			kml = """<?xml version="1.0" encoding="UTF-8"?>
			<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
			<Document>
				<name>RTPosition.kml</name>
				%s
			</Document>
			</kml>""" % string
			target = open('RT_Position.kml', 'w')
			target.truncate() 
			target.write(kml)
			target.close()
	
	# ------------------------------------------------------------- WAIT FOR MORE DATA -----------------------------------------------------------------
	else:
		print('No More Data...\n')
		raw_input('Exit Loop\n>>> ')
		# exit loop
		break
		
pyplot.show(block=False)
raw_input("CLose Figures\n>>> ")


	

	
	
	
