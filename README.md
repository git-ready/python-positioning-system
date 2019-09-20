# Python-Positioning-System
Inputs: latitude, longitude, altitude, and signal TOF.  Algorithm: least squares.  Output: position in Google Earth  


Instructions for Running FindMe.py for Windows, Python Version 2.7

Contact: Michael Phillips | mailtwomike@gmail.com | (724) 263-0292

1) download and install python 2 from http://python.org/download

2) open PowerShell and enter this: [ENVIRONMENT]::SETENVIRONMENTVARIABLE("PATH", "$ENV:PATH;C:\PYTHON27", "USER")

3) close PowerShell and open it again, type "python" and press "Enter", you should see: 
	PS C:\Users\mphillips> python
	Python 2.7.16 (v2.7.16:413a49145e, Mar  4 2019, 01:30:55) [MSC v.1500 32 bit (Intel)] on win32
	Type "help", "copyright", "credits" or "license" for more information.
	>>>
	
4) To quit python press "Ctrl-C"

5) Install the extra python packages using "python -m pip install [package-name]":
	i) open PowerShell, enter the following lines:
	ii)    python -m pip install numpy
	iii)   python -m pip install scipy
	iv)    python -m pip install matplotlib
	v)     python -m pip install mpl_toolkits
	vi)    python -m pip install math
	vii)   python -m pip install time
	viii)  python -m pip install random
	
6) Download Google Earth from: https://www.google.com/earth/versions/

7) Open Google Earth

7) Download Notepad++ (if you want to edit the python scripts)

8) Copy the "Python" folder to your desktop:
	a) Open Powershell type "cd desktop" press enter
	b) type "cd python" press enter
	c) type "dir" press enter and you should see:
	
			Windows PowerShell
			Copyright (C) Microsoft Corporation. All rights reserved.

			PS C:\Users\mphillips> cd desktop
			PS C:\Users\mphillips\desktop> cd python
			PS C:\Users\mphillips\desktop\python> dir


				Directory: C:\Users\mphillips\desktop\python


			Mode                LastWriteTime         Length Name
			----                -------------         ------ ----
			-a----        3/31/2019  12:09 PM         379845 Capture1.JPG
			-a----        3/31/2019  11:00 AM          15290 FindMe.py
			-a----        3/28/2019   1:28 PM           2961 Find_Me_Functions.py
			-a----        3/29/2019   2:57 PM           1341 Link.kml
			-a----        3/31/2019  11:46 AM           1310 READ_ME.txt


			PS C:\Users\mphillips\desktop\python>
			
	(d) type "cls" and press enter, to clear the screen
	
	(e)  type "python findme.py" and press enter to Run, you should see:
			
			PS C:\Users\mphillips\desktop\python> python findme.py

			Displaying Planned Flight
			>>>
	(f) in the python folder on the desktop double click 
	
	the "Link.kml" google earth file, you should see the planned 
	     flight path and "your" position in google earth.

	(g) go back to the PowerShell screen. 
			(TIP 1: to prevent program from crashing, you can minimize the 3d plots but be sure not to "X" out of them)
			(TIP 2: to keep the program running, you need to remain "inside" of the Powershell screen, so when you open the 
					google earth window be sure to re-enter the Powershell Screen)
	
	(h) Press Enter in the Powershell, you can minimize the "Planned Flight Path" and "Range Data vs. Time" plots
		   but keep the "Least Squares Lateration" Plot and the Powershell screen open on top of the google earth screen.
	
	(i) Enter 1 or 2 in Powershell screen to use the noisy or exact range data
	(j) Your screen should look like "Capture1.jpeg"
	(k) Press enter to Run
	(l) When running the first time you will have to either re-load the Link.kml file or refresh the links inside google earth.
	    Once you get all the links loaded once you shouldn't have to mess with it anymore.
	(m) The program should start processing the data and update google earth plots in real time. 
	(n) To quit the program before it ends press "Ctrl-C" in the PowerShell window.

9) In the FindMe.py script:
		lines 43-53 change the initial parameters for the flight pattern and your location.
		lines 57-62 change the shape of the elliptical flight pattern
		line 72 changes the noise fluctuation in the range data
		line 265 changes the view angle ratio requirement (if you make it bigger than 10 the predictions seem to get pretty bad)
		
