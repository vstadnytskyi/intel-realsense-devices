============
Device
============

The driver class provides ...


.. code-block:: python

   import intel_realsense_devices
   print(f'current version of the library is {intel_realsense_devices.__version__}')
   from intel_realsense_devices.driver import Device
   device = Device(config_filename = "YOUR CONFIG YAML FILE", h5py_filename = "YOUR H5PY/HDPY FILE NAME")
   device.init()

Your config yaml file must contain a serial number

.. code-block:: yaml
   serial_number: "YOUR SERIAL NUMBER"


If you dont have a congfi yaml file:
.. code-block:: python
   
   import intel_realsense_devices
   print(f'current version of the library is {intel_realsense_devices.__version__}')
   from intel_realsense_devices.driver import Device
   device = Device(config_filename = "", h5py_filename = "YOUR H5PY/HDPY FILE NAME")
   device.serial_number = "YOUR SERIAL NUMBER"
   device.init()

The device class automaically inizlizes the driver class when init() func is called that is why a serial number 
is needed. It then inializes a dict of circular buffers to collect different imgs/data from the camera.






