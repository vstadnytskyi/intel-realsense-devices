======
Stream
======

Higher level application that can stream live images/data from the camera and data from the circular buffer.

These are the different functions that you can run: 

 * To show a live stream of depth, infrared, and color using the matplotlib library:

 .. code-block:: python

    stream.plt_live_stream()

 * To show a live plot of the IMU readings:

  .. code-block:: python

      stream.IMU_live_plotting(dt = 1)

 * To stream data that is already stored into the buffer as a replay.

  .. code-block:: python

      stream.stream_buffer()

 * To livestream the data as it is coming in from the circular buffers:

  .. code-block:: python

      stream.cv2_live_stream_buffer()


