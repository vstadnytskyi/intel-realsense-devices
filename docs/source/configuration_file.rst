===================
Configuration File
===================

There are two main key points of the configuration file. There must be serial number parameter and a channel parameter that is a list.
There is a configuration file template in the test_file directory to model after. 

* THE PAREAMETER NAMES MUST BE KEPT THE SAME.

* There must be a serial_number parameter.
EX:

.. code-block:: yaml

    serial_number: "f1231322"

=====================
Channels parameter 
=====================

.. code-block:: yaml

    channels:
      - #<- channel entery 

- The Channel parameter is a list with each element contaning a dictioniry of parameters.
- If a channel parameter is not defined then default values will be used.
- There must be an entry for each differnt type of channel.
- There are 5 parameter for an image channel, and 3 for the IMU. 

Example of an element:

.. code-block:: yaml

  - #<-this is first entry in the channels list
    type: depth
    fps: 30
    buffer_length: 30
    buffer_shape: (480, 640)
    buffer_dtype: unit16


* NOTE: THE CHANNEL ENTERY ORDER MUST BE KEPT IN THE SAME ORDER.

0 -> depth
1 -> color
2 -> infrared
3 -> accel
4 -> gyro

Example of a IMU entry. 

.. code-block:: yaml

  - 
    type: accel
    fps: 200
    buffer_length: 30000



* Defualt values

- The buffer length will be set to 10 for images and 10000 for IMU data.
- Accel default fps set to 200, Gyro defualt fps set to 400
