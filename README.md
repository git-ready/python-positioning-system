# Python-Positioning-System

Inputs: latitude, longitude, altitude, message TOF  |  Algorithm: least squares or multilateration |  Output: position in Google Earth  

The Question: If you are given a computer on the ground that has no gps connection, but has a map of the world (Google Earth), and a wireless connection to a gps-connected drone flying approx. 50 miles away, can your computer determine your position in Google Earth?

The Answer: In theory, yes. The the Findme.py program runs a simulation of this scenario. Even with a random noise background of (+/-5 meters) injected to the (Time of Flight x Speed of Light) data, the least squares algorithm still produces good predictions with as little as 10 data points from the simulated flight path. The prediction becomes better with more data points and/or with a bigger field of view (greater angle between points) and with a smaller noise background. The multilateration algorithm takes 4 data points that are positioned far apart (the further the better) and calculates position. The two algorithms are defined in the Find_Me_Functions.py.

Assumptions: (1) PTP (the precision time protocol) is running between the flight and ground computers, and (2) the computers are capable of producing accurate enough timestamps (timestamp precision 10x > than TOF) for incoming and outgoing messages. This level of clock syncronization is nessesary to determine accurate time of flight (TOF) between the flight and ground computer. The difference beetween the timestamps is the TOF.

To install and run the simulator on windows with python 2.7 see Install.txt

To understand the multilateration calculation see section 3.3 of Trilateration.pdf
For least squares see the scipy --> optimize --> least_squares, and https://en.wikipedia.org/wiki/Least_squares
