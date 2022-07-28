============
Recorder
============

This file is a script that takes in two filenames names, a config and h5py file.

To intialize The recorder:

.. code-block:: python

    import intel_realsense_devices
    print(f'current version of the library is {intel_realsense_devices.__version__}')
    from intel_realsense_devices.recorder import recorder
    record = Recorder(config_filename = "YOUR CONFIG YAML FILE", h5py_filename = "YOUR H5PY FILENAM")


To show a live stream of depth, infarared, and color run the following command:

.. code-block:: python
   record.live_stream_test()

To show live plot of the gyro and accelerometer run the following command:

.. code-block:: python
    record.show_live_plotting(dt = 1)