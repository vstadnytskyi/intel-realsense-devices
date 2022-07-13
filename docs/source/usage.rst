=====
Usage
=====

The driver class is configured to run for the realsense install L515 and D435.
it may run with other modules but some functionality will give breakdown

Please see config_template.conf to see how to structure your config file.

You should be in the intel-realsense-devices directory.

To intialize device:

.. code-block:: python

   import intel_realsense_devices
   print(f'current version of the library is {intel_realsense_devices.__version__}')
   from intel_realsense_devices.device import Device
   device = Device(config_filename = "YOUR CONFIG YAML FILE", h5py_filename = "YOUR H5PY/HDPY FILE NAME")
   device.init()

Your config yaml file must contain a serial number and imgs_to_collect in order to prepare early. This contatins the number of images 
you want to collect from the camera. This will be used as the size for the ciruclar buffer. Since the 
gyroscope and accelerometer collect data at a higher frequency the size of the circular buffer will need be
accounted for.

.. code-block:: yaml

   serial_number: "YOUR SERIAL NUMBER"
   imgs_to_collect: "NUMBER OF IMAGES TO COLLECT"


If you dont have a congfi yaml file, you can run it by setting the serial number later on (see below). If there is no config file given
images_to_collect will be set to 100 by default. In order to avoid that ou should create a config file.

.. code-block:: python
   
   import intel_realsense_devices
   from intel_realsense_devices.device import Device
   device = Device(config_filename = "", h5py_filename = "YOUR H5PY/HDPY FILE NAME")
   device.serial_number = "YOUR SERIAL NUMBER"
   device.init()

****************
Collecting Data
****************

All the functionality to collect data and store it in a file is already done for you.
All you have to do is specify how many images you want to collect.
Right now it works on time, it still needs to be updated.

.. code-block:: python          
    
    device.collect_data(time = "an integer") # still needs to be updated

After it collects the data it needs it then saves the data to a H5PY file where there is a data set 
for ['accel', 'color', 'depth', 'gyro', 'infrared'].