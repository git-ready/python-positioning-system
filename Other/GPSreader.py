# -*- coding: utf-8 -*- 
import serial
import pynmea2
from sys import argv

script, filename = argv
print "Connect to GPS? Press C: ",
go = raw_input()
if go == 'C' or 'c':

	print "Connecting to 'COM3' serial port..."
	test = serial.Serial('COM3').readline() # read a  random sentence from the port
	if test.split('G',1)[0]=='$': #NMEA sentences all begin with the $ sign
		
		with serial.Serial( port='COM3', baudrate=9600, timeout=1) as gps: # Opening GPS data feed object. 9600bits/sec is COM3's baudrate from tera term. 
			print "Connected to: %s. Data Looks Good, Saving to %s..." % (gps.name, filename)
			
			target = open(filename, 'w') # Create the file to save the data
			
			while True:
				
				msg = gps.readline() # Reads one line
				if msg.startswith('$GPVTG', 0, 6):
					target.write(msg)
					target.write('\n')
				
				elif msg.startswith('$GPGGA', 0, 6):
					target.write(msg)
					msg2 = pynmea2.parse(msg)
					print 'Zulu Time: %s' % (msg2.timestamp)
					print 'Latitude:  %ideg %.2fmin %.2fsec %s' % (msg2.latitude, msg2.latitude_minutes, msg2.latitude_seconds, msg2.lat_dir)
					print 'Longitude: %ideg %.2fmin %.2fsec %s' % (msg2.longitude, msg2.longitude_minutes, msg2.longitude_seconds, msg2.lon_dir)
					print 'Elevation: %r %r (Above Mean Sea Level)' % (msg2.altitude, msg2.altitude_units)
					print 'Fix Quality: %r' % msg2.gps_qual
					print 'Horizontal Dilution of Precision: %r' % msg2.horizontal_dil
					print 'Number of Tracked Satellites: %r \n' % msg2.num_sats
				else:
					target.write(msg)
					
	else:
		print "GPS connection failed:\n\t try running again\n\t check USB Connection\n\t check 'Device Manager' for port number"
else:
	print "No Connection."
	
	