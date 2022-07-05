============
Driver
============

The driver class is configured to run for the realsense intell L515 and D435.

The driver class provides ...


.. code-block:: python

   import intel_realsense_devices
   print(f'current version of the library is {intel_realsense_devices.__version__}')
   from intel_realsense_devices.driver import Driver
   driver = Driver()
   driver.init(serial_number="YOUR SERIAL NUMBER")

To check what device current driver is connected

.. code-block:: python

   driver.print_device_info()

To see if there are other devices currently connected to your PC 

.. code-block:: python
   
   print(driver.find_devices())

In order to test if your device is connected and color image and depth piplines are configured run:

.. code-block:: python
   
   driver.live_stream_test()
