"""
Driver for intel realsense devices. This file contains simple wrappers for functions provided by Intel SDK.
https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples
https://dev.intelrealsense.com/docs/python2

Currently supports:
Intel LiDAR L515
Intel Depth Camera D435i

The driver 
"""

import numpy as np 
from time import time, sleep

DEPTH = "depth"
COLOR = "color"
INFRARED = "infrared"
GYRO = "gyro"
ACCEL = "accel"
IMAGE = "image"
FRAMEN = "frameN"

DEPTHCHANNEL = 0
COLORCHANNEL = 1
INFARAREDCHANNEL = 2
ACCELCHANNEL = 3
GYROCHANNEL = 4
BUFFERLENGTH = "buffer_length"


class Device():
    """ 
    Higher level class that collects different image data to store in a circular buffer
    
    """
    def __init__(self, config_filename):
        """
        part 1 to initialize the camera
        
        Parameters:
        ------------
        config_filename: string
            config file path

        h5py_filename: string
            h5py file path
        """

        # Create a context object. This object owns the handles to all connected realsense devices  
        self.config_dict = {}
        self.buffers = {}
        self.threads = {}
        self.serial_number = ""
        self.run = False
        self.io_push_queue = None
        self.io_put_queue = None
        self.read_config_file(config_filename)
        
    def init(self):
        """
        Import intel real sense driver and initializes the device.
        Initialize Circular buffers that contain data for each frame type
        """

        from intel_realsense_devices.driver import Driver
        self.driver = Driver()
        self.driver.init(self.config_dict)

        default_buffer_length = 10
        # if channels are empty
        if self.config_dict["channels"] == None:
            channels = self.config_dict["channels"] = [
                {'buffer_length': default_buffer_length},
                {'buffer_length': default_buffer_length},
                {'buffer_length': default_buffer_length},
                {'buffer_length': default_buffer_length * 10000},
                {'buffer_length': default_buffer_length * 10000}
            ]
        else:
            channels = self.config_dict["channels"] # list of the channels
       
               
        # intialialize the circular buffer
        from circular_buffer_numpy.circular_buffer import CircularBuffer
        self.buffers[DEPTH] = CircularBuffer(shape = (channels[DEPTHCHANNEL][BUFFERLENGTH],)+ (480, 640), dtype = "uint16") 
        self.buffers[COLOR] = CircularBuffer(shape = (channels[COLORCHANNEL][BUFFERLENGTH],)+ (540, 960,3), dtype = "uint8") 
        self.buffers[INFRARED] = CircularBuffer(shape = (channels[INFARAREDCHANNEL][BUFFERLENGTH],)+ (480, 640), dtype = "uint8") 
        self.buffers[GYRO] = CircularBuffer((channels[GYROCHANNEL][BUFFERLENGTH],5), dtype = 'float64')
        self.buffers[ACCEL] = CircularBuffer((channels[ACCELCHANNEL][BUFFERLENGTH],5), dtype = 'float64')
        self.buffers[FRAMEN] = CircularBuffer(shape = (channels[COLORCHANNEL][BUFFERLENGTH],), dtype = "int") 

    def read_config_file(self, config_filename):
        """
        reads configuration file and returns dictionary of parameters. The configuration file is created using YAML.

        Parameters
        ----------
        filename : string
            path to configuration file

        """
        import yaml
        
        if config_filename == "":
            return
        with open(config_filename) as f:
            self.config_dict = yaml.safe_load(f)
            self.serial_number = self.config_dict["serial_number"]
        

    def start(self):
        """
        orderly start of device operation
        """
        from ubcs_auxiliary.multithreading import new_thread
        self.run = True
        self.threads[GYRO] = new_thread(self.run_get_gyro)
        self.threads[ACCEL] = new_thread(self.run_get_accel)
        self.threads[IMAGE] = new_thread(self.run_get_images)
        
    def stop(self):
        """
        orderly stop of device operation
        """
        self.run = False 


    def run_once_images(self):
        """
        Acquires one set of image data and apends them in separate circular buffers.
        """
        img_data_dict = self.driver.get_images()
        
        self.buffers[DEPTH].append(img_data_dict[DEPTH].reshape((1,) + img_data_dict[DEPTH].shape))
        self.buffers[COLOR].append(img_data_dict[COLOR].reshape((1,) + img_data_dict[COLOR].shape))
        self.buffers[INFRARED].append(img_data_dict[INFRARED].reshape((1,) + img_data_dict[INFRARED].shape))
        self.buffers[FRAMEN].append(img_data_dict[FRAMEN].reshape((1)))

    def run_once_gyroscope(self):
        """
        Acquires one set of gyroscope reading and saves them in gyroscope related circular buffer.
        """

        f = self.driver.pipeline[GYRO].wait_for_frames()
        gyro = (f[0].as_motion_frame().get_motion_data())
        frameN = f[0].as_motion_frame().frame_number
        t = time()
        gyro_array = np.asanyarray((t,frameN,gyro.x,gyro.y,gyro.z)).reshape(1,5)
        self.buffers[GYRO].append(gyro_array)

    def run_once_accelerometer(self):
        """
        Acquires one set of gyroscope reading and saves them in gyroscope related circular buffer.
        """

        f = self.driver.pipeline[ACCEL].wait_for_frames()
        accel = (f[0].as_motion_frame().get_motion_data())
        frameN = f[0].as_motion_frame().frame_number
        t = time()
        accel_array = np.asanyarray((t,frameN,accel.x,accel.y,accel.z)).reshape(1,5)
        self.buffers[ACCEL].append(accel_array)

    def run_get_gyro(self):
        while self.run:
            self.run_once_gyroscope()
            
    def run_get_accel(self):
        while self.run:
            self.run_once_accelerometer()

    def run_get_images(self):
        while self.run:
            self.run_once_images()
            

    def io_push(self, io_dict = None):
        """
        Add dictionary with key-value pairs every time you want a value to be pushed
        to server for processing. 
        
        Parameters: 
        ------------
        io_dict : dict
            Where key is Process Variable name and value is new value 
        """
        
        if self.io_push_queue is not None:
            self.io_push_queue.put(io_dict)

    def io_pull(self, io_dict):
        """
        Io_pull, takes dictionary as input where key is Process Variable name and value is 
        new value. This is a path we use for server to submit updates back to the device level.
        Again see simple DAQ example.       
       
        Parameters: 
        ------------
        io_dict : dict
            Where key is Process Variable name and value is new value 
        """
        while True:
            io_dict.get(lock = True)
            for key, value in io_dict.items():
                if key == "laser intensity":
                    self.driver.set_laser_intensity(value)
                


if __name__ == "__main__":
    """
    For testing
    """
    import logging
    from logging import debug, info, warning, error
    logging.getLogger("blib2to3").setLevel(logging.ERROR)
    logging.getLogger("parso").setLevel(logging.ERROR)
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    logging.getLogger("PIL").setLevel(logging.ERROR)
    logging.getLogger("asyncio").setLevel(logging.ERROR)
    
    import sys

    if len(sys.argv) > 1:
        debug('reading specified config file')
        config_filename = sys.argv[1]
        info(config_filename)
    else:
        debug('reading default config file')
        # config_filename = r"C:\Users\Abdel Nasser\Documents\L151 Camera\intel-realsense-devices\intel_realsense_devices\test_files\config_d435i__139522074713.yaml"
        config_filename = "test_files\config_L151_f1320305.yaml"
        info(config_filename)

    from tempfile import gettempdir
    import os
    log_filename = os.path.join(gettempdir(),'intel_realsense_device.log')
    logging.basicConfig(filename=log_filename,
                level=logging.DEBUG,
                format="%(asctime)-15s|PID:%(process)-6s|%(levelname)-8s|%(name)s| module:%(module)s-%(funcName)s|message:%(message)s")

    device = Device(config_filename = config_filename)
    device.init()








