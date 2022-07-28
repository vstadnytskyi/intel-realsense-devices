============
Device
============

Device is a higher level class that will contains functionality to collect data from the camrea. 

To intialize device:

.. code-block:: python

   import intel_realsense_devices
   print(f'current version of the library is {intel_realsense_devices.__version__}')
   from intel_realsense_devices.device import Device
   device = Device(config_filename = "YOUR CONFIG YAML FILE")
   device.init()


The main attriubtes of this class are the buffers and threads dicts. It runs multi-threads that continusly collect data
from different pipelines such as gyroscope and accelerometer. It then stores them in a sepereate circular buffers. 

