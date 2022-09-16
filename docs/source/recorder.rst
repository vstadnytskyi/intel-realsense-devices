============
Recorder
============

This is a higher level application that records and stores in live images/data from the camera.
 
The recorder can either be ran as a script using arguments or can be ran as a module.
 
To run the recorder as a script using arguments:
 
.. code-block:: python
 
    import intel_realsense_devices
    print(f'current version of the library is {intel_realsense_devices.__version__}')
    python recorder.py "YOUR CONFIG FILE" "YOUR H5PY FILE"

To run the recorder as a module:

.. code-block:: python

    import intel_realsense_devices
    from intel_realsense_devices.higher_applications.recorder import Recorder
    recorder = Recorder("YOUR CONFIG FILE", "YOUR H5PY FILE")
    recorder.start()
    recorder.save_h5py_file()
    recorder.stop()

How it runs
------------

Recorder starts out by initializing the lower level classes. The script then starts the recorder. 

.. code-block:: python
 
    recorder.start()
    
The start function starts the device and creates a thread running the record function. It then runs a live
stream on the main thread. The record function continues to run the device until it receives enough frames,
which is the length of the frame buffer length.
 
On the main thread it runs:
 
.. code-block:: python
 
    stream.cv2_live_stream_buffer()
 
This is a function in the stream module that live streams the last image insereted into the circular buffers.
This uses the cv2 library instead of the matplotlib library. The cv2 library can render faster then the plt, 
so there are no delays. This is also beneficiary as we won't have to worry about skipping frames due to the
matplotlib taking time to render images.
 
It then saves data into a H5py file with:
 
.. code-block:: python
 
    recorder.save_h5py_file()
 
This function takes the data from the circular buffers and creates the following data sets to store them in:

.. code-block:: python

  ['accel', 'color', 'depth', 'frameN', 'gyro', 'infrared']


It then orderly shutsdown the lower level of the system

.. code-block:: python
 
    recorder.stop()
 