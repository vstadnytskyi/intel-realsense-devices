=====
Usage
=====
 
The driver class is deisgned to run the intel realsense cameras. It is specifically designed to run L151 and D435i.
it may run with other models but some functionaity may break down.

System design:

* Driver: The lowest level that communicates with the cameras.
* Device: Runs multi-threads to retrieve images then stores them into circular buffers. 
* Recorder: Runs the whole system to collect and store data. 

Running the system
-------------------

In order to run the applications, you should be in the intel-realsense-devices directory.
 
To initialize device:
 
.. code-block:: python
 
   import intel_realsense_devices
   print(f'current version of the library is {intel_realsense_devices.__version__}')
   from intel_realsense_devices.device import Device
   device = Device(config_filename = "YOUR CONFIG YAML FILE")
   device.init()
   
Your config yaml file must contain a serial number and channels parameter in order to avoid
using the default values. Please see configuration_file.rst for more information on structuring your config file.

IMU settings
------------

Since the gyroscope and accelerometer collect data at a higher frequency the size of the circular buffer will need to be accounted for.

For the D435i camera:

* Acceleration Output Data Rate 62.5Hz/250Hz
* Gyro Output Data Rate at 200Hz/400Hz
 
For the L515 camera:

* Acceleration Output Data Rate 100Hz/200Hz/400Hz
* Gyroscope Output Data Rate 100Hz/200Hz/400Hz

Applications
-------------
There are two different applications:

* Recorder

The recorder is able to collect data while livestreaming it. You can find more information in recorder.rst

* Stream

There are diffent functionalities in this class such as live streaming images using different python modules and live ploting of IMU data. You can find more information in stream.rst.

Recorder
---------------
 
All the functionality to collect data and store it in a file is already done for you in the record script.
In order to run it, you will need a config file and a h5py file to save data into.
 
To collect the data run the following script:
 
.. code-block:: python    

      import intel_realsense_devices

      # IT MUST BE IN THIS ORDER  
      python recorder.py "YOUR CONFIG FILE" "YOUR H5PY FILE"
      # my example
      python recorder.py "test_files\config_L151_f1320305.yaml" "test_files\test.h5py"
 
 
The data will be stored into a H5PY file where the dataset names are ['accel', 'color', 'depth', 'frameN', 'gyro', 'infrared'].
 
 

