============
Examples
============

The examples sub directory contains different scripts for running different types of cameras.
Some cameras can be used in scripts that arent meant for it as thoses cameras ontain thoses basic
functionality and more. The serial number is pre defined as a global variable.
That will have to be changed in order run with your own camera.

simple_l515.py 
-------------------

Runs a basic sets up a single pipline that collects color, depth, and infared data
from the camera and creates a live stream of thoses 3 images.

simple_l515_multiple_piplines.py
----------------------------------

Runs a script that sets up multiple piplines to collect data from the gyroscope and accelerometer.
It then plot that data x, y, z data on to a figure.

simple_R435i.py
----------------------

runs a script that caputers a depth and color image, then displays both onto a figure. In another figure it plots slices 
of depth image onto a xy plane. Lastly it saves the color/depth data into a txt file in the test_files sub-directory.
