============
Device
============

Device is a higher level class that contains functionality to collect data from the camera. 

To set up and intialize device:

.. code-block:: python

   import intel_realsense_devices
   print(f'current version of the library is {intel_realsense_devices.__version__}')
   from intel_realsense_devices.device import Device
   device = Device(config_filename = "YOUR CONFIG YAML FILE")
   device.init()


The main attriubtes of this class are to set up the ciruclar buffers and run threads. 
It runs multi-threads that continusly collect data from different pipelines. 
It then stores them in a sepereate circular buffers. 

