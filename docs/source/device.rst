============
Device
============

Device is a higher level class that will contains funcanitly to collect data from the different piplines
such as gyroscope and accelerometer. It runs multi-threads that continusly collect data. 

To intialize device:

.. code-block:: python

   import intel_realsense_devices
   print(f'current version of the library is {intel_realsense_devices.__version__}')
   from intel_realsense_devices.device import Device
   device = Device(config_filename = "YOUR CONFIG YAML FILE", h5py_filename = "YOUR H5PY/HDPY FILE NAME")
   device.init()


To test if everything was setup correctly there is a function called show_live_plotting_test() that shows
 a live plotting of the gyroscope and accelerometer from the camera to test if everything is setup corretly. 

.. code-block:: python
   
   device.show_live_plotting_test(dt = 1)


