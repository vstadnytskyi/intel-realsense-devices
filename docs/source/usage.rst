=====
Usage
=====

The driver class is configured to run for the realsense install L515 and D435.
it may run with other modules but some functionality will give breakdown

Start by importing intel realsense devices and inializing the device

.. code-block:: python

    from intel_realsense_devices.driver import Device
    device = Device(config_filename = "YOUR CONFIG YAML FILE", h5py_filename = "YOUR H5PY/HDPY FILE NAME")
    device.init()


****************
Collecting Data
****************

All the functionality to collect data and store it in a file is already done for you.
All you have to do is specify how many images you want to collect.
Right now it works on time, it still needs to be updated.

.. code-block:: python          
    
    device.collect_data(time = "an integer") # still needs to be updated


In the config file there is a paremeter, imgs_to_collect, that contatins the number of images you want to collect 
from the camera. This will be used as the size for the ciruclar buffer. Since the gyroscope and 
accelerometer collect data at a higher frequency the size of the circular buffer will be accounted 
for.


.. code-block:: yaml  

    imgs_to_collect = "NUMBER OF IMAGES TO COLLECT"

After it collects the data it needs it then saves the data to a H5PY file where there is a data set 
for ['accel', 'color', 'depth', 'gyro', 'infrared'].