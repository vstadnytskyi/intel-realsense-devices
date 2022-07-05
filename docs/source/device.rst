============
Device
============

To intialize device

.. code-block:: python

   import intel_realsense_devices
   print(f'current version of the library is {intel_realsense_devices.__version__}')
   from intel_realsense_devices.device import Device
   device = Device(config_filename = "YOUR CONFIG YAML FILE", h5py_filename = "YOUR H5PY/HDPY FILE NAME")
   device.init()

Your config yaml file must contain a serial number

.. code-block:: yaml

   serial_number: "YOUR SERIAL NUMBER"


If you dont have a congfi yaml file, you can run it this way:

.. code-block:: python
   
   import intel_realsense_devices
   from intel_realsense_devices.device import Device
   device = Device(config_filename = "", h5py_filename = "YOUR H5PY/HDPY FILE NAME")
   device.serial_number = "YOUR SERIAL NUMBER"
   device.init()

The device class automaically inizlizes the driver class when init() is called that is why a serial number 
is needed.

In order to test if gyroscope and accelerometer are configured run the following command:

.. code-block:: python
   
   device.show_live_plotting_test(dt = 1)


