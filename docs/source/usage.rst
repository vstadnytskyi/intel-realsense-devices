=====
Usage
=====

The driver class is configured to run for the realsense install L515 and D435i.
it may run with other modules but some functionality will breakdown

You should be in the intel-realsense-devices directory.

To intialize device:

.. code-block:: python

   import intel_realsense_devices
   print(f'current version of the library is {intel_realsense_devices.__version__}')
   from intel_realsense_devices.device import Device
   device = Device(config_filename = "YOUR CONFIG YAML FILE")
   device.init()

Your config yaml file must contain a serial number and channels paramter in order to avoid 
using the defualt values. In the channels paremter there should be a dict for each frame type. 
This contains the buffer_length. This will be used as the size for the ciruclar buffer. 

Since the gyroscope and accelerometer collect data at a higher frequency the size of the
circular buffer will need be accounted for.

Please see config_template.conf for a more more descriptive structure.

.. code-block:: yaml

   serial_number: "YOUR SERIAL NUMBER"
   channels:
      - #<-this is first entry in the channels list
         type: depth # frame type
         fps: 30 
         buffer_length: 30


For the D435i camera:
Acceleation Output Data Rate 62.5Hz/250Hz
Gyro Output Data Rate at 200Hz/400Hz

For the L515 camera:
Accelerometer Output Data Rate 100Hz/200Hz/400Hz
Gyroscope Output Data Rate 100Hz/200Hz/400Hz

****************
Collecting Data
****************

All the functionality to collect data and store it in a file is already done for you in the record script.
In order run it all you need is a config file and a h5py file to save data into.

To collect the data run the following script.

.. code-block:: python        
      # IT MUST BE IN THIS ORDER  
      python recorder.py "YOUR CONFIG FILE" "YOUR H5PY FILE"
      # my example
      python recorder.py "test_files\config_L151_f1320305.yaml" "test_files\test.h5py"


The data will be stored into a H5PY file where the data set names are ['accel', 'color', 'depth', 'frameN', 'gyro', 'infrared'].
