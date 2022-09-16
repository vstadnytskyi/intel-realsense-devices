======
Stream
======

Higher level application that can stream live images/data from the camera and data from the circular buffer.

These are the different functions that you can run: 

 * To show a live stream of depth, infrared, and color using the matplotlib library:

 .. code-block:: python

    record.plt_live_stream()

 * To show a live plot of the IMU readings:

  .. code-block:: python

      record.IMU_live_plotting(dt = 1)

 * To stream data that is already stored into the buffer as a replay.

  .. code-block:: python

      recorder.stream_buffer()

 * To livestream the data as it is coming in from the circular buffers:

  .. code-block:: python

      recorder.cv2_live_stream_buffer()


