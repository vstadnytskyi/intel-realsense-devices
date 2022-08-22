============
Recorder
============
 
This file is a script that takes in two file names names as arguments, a config and h5py file.
 
To initialize the recorder:
 
.. code-block:: python
 
    import intel_realsense_devices
    print(f'current version of the library is {intel_realsense_devices.__version__}')
    python recorder.py "YOUR CONFIG FILE" "YOUR H5PY FILE"
 
Recorder starts out by initializing the device class. The script then starts the recorder. Running the following line.
 
.. code-block:: python
 
    recorder.start()
 
The start function starts the device and creates a thread running the record function. It then runs a live
stream on the main thread. The record function continues to run the device until it receives enough frames,
which is the length of the frame buffer length.
 
On the main thread it runs:
 
.. code-block:: python
 
    recorder.cv2_live_stream()
 
This is a live stream of the latest images stored in the circular buffers. This uses the cv2 library instead of the
matplotlib library. The main reason for this is is because it can render faster so there are no delays when displaying
live feed. This is also beneficiary as we won't have to worry about skipping frames due to the matplotlib taking some time
to render images.
 
It then saves data into a H5py file.
 
.. code-block:: python
 
    recorder.save_h5py_file()
 
This function takes the device circular buffers and creates the following data sets:
['accel', 'color', 'depth', 'frameN', 'gyro', 'infrared']
 
 
=================
Other Functions
=================
 
 
.. code-block:: python
 
   record.plt_live_stream()
 
To show a live stream of depth, infrared, and color using the matplotlib library.
 
 
.. code-block:: python
 
    record.show_live_plotting(dt = 1)
 
To show live plot of the gyro and accelerometer:
 
.. code-block:: python
 
    recorder.stream_buffer()
 
Streams the images in the buffer as a replay. This is useful if you want to
see the images stored in the buffer.
 
.. code-block:: python
 
    recorder.read_h5py_file
 
This function reads the hp5y file data sets, For testing purposes.

