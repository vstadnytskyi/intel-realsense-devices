============
Driver
============

* The driver class is configured to run for the realsense intel L515, D435i and D455 cameras.

To set up a driver:

.. code-block:: python

   import intel_realsense_devices
   print(f'current version of the library is {intel_realsense_devices.__version__}')
   from intel_realsense_devices.driver import Driver
   config_filename = "YOUR CONFIG FILE NAME"
   with open(config_filename) as f:
      config_dict = yaml.safe_load(f)
      driver.init(config_dict)


To check what device current driver is connected:

.. code-block:: python

   driver.print_device_info()

To see if there are other devices currently connected to your PC:

.. code-block:: python
   
   print(driver.find_devices())

In order to test if your device is connected and color image and depth piplines are configured:

.. code-block:: python
   
   driver.live_stream_test()

Set laser intensity function:

.. code-block:: python
   
   driver.set_laser_intensity(laser_power = "int")


If the laser intensity is too strong, the reciver will saturate similairly to
how a image can be overexposed. If it's too weak the system fails to get any information. 
Adjusting the laser power manually may give better results considering 
the specific distance and objects for the use case. 
The defualt/average value of the laser is 150 mw. The range in which laser intensity can be set is from 0-100%. 