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
from time import time, ctime, sleep

import h5py

DEPTH = "depth"
COLOR = "color"
INFRARED = "infrared"
GYRO = "gyro"
ACCEL = "accel"
IMAGE = "image"
FRAMEN = "frameN"


class Device():
    """ 
    Higher level class that collects image data to store in a circular bufferip[]
    
    """
    def init(self):
        """
        Import intel real sense driver and initializes the device.
        Initialize Circular buffers that contain data for each frame type
        """
    
        from intel_realsense_devices.driver import Driver
        self.driver = Driver()
        self.driver.init(self.serial_number)
    
        # if the config dict is empty
        if self.config_dict == {}:
            imgs_to_collect = 100
        else:
            imgs_to_collect = self.config_dict['imgs_to_collect'] # number of images to collect 

        # intialialize the circular buffer
        from circular_buffer_numpy.circular_buffer import CircularBuffer
        self.buffers[DEPTH] = CircularBuffer(shape = (imgs_to_collect,)+ self.driver.get_image_shape(DEPTH), dtype = self.driver.get_image_dtype(DEPTH)) 
        self.buffers[COLOR] = CircularBuffer(shape = (imgs_to_collect,)+ self.driver.get_image_shape(COLOR), dtype = self.driver.get_image_dtype(COLOR)) 
        self.buffers[INFRARED] = CircularBuffer(shape = (imgs_to_collect,)+ self.driver.get_image_shape(INFRARED), dtype = self.driver.get_image_dtype(INFRARED)) 
        self.buffers[GYRO] = CircularBuffer((30000,5), dtype = 'float64')
        self.buffers[ACCEL] = CircularBuffer((30000,5), dtype = 'float64')
        self.buffers[FRAMEN] = CircularBuffer(shape = (imgs_to_collect,), dtype = "int") 


    def __init__(self, config_filename, h5py_filename):
        """
        part 1 to iniatilie the camera

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
        self.run = True
        self.serial_number = ""
        self.h5py_filename = h5py_filename
        self.io_push_queue = None
        self.io_put_queue = None
        self.read_config_file(config_filename)
        

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
        
        self.threads[GYRO] = new_thread(self.run_get_gyro)
        self.threads[ACCEL] = new_thread(self.run_get_accel)
        self.threads[IMAGE] = new_thread(self.run_get_images)

    def stop(self):
        """
        orderly stop of device operation
        """
        self.run = False 
        self.driver.stop() #shuts down the piplines 


    def save_h5py_file(self, filename):
        """
        saves the data from the buffers into h5py file
        Parameters
        ----------
        filename : string 
            path to H5py file
        
        """
        # grab all the data in the circular buffer
        gyro_data = self.buffers[GYRO].get_all()
        accel_data = self.buffers[ACCEL].get_all()
        depth_data = self.buffers[DEPTH].get_all()
        infrared_data = self.buffers[INFRARED].get_all()
        color_data = self.buffers[COLOR].get_all()
        frameN_data = self.buffers[FRAMEN].get_all()

        # write data in the H5PY file
        with h5py.File(filename, 'w') as f:
            dset = f.create_dataset(GYRO, data = gyro_data)
            dset = f.create_dataset(ACCEL, data = accel_data)
            dset = f.create_dataset(DEPTH, data = depth_data)
            dset = f.create_dataset(COLOR, data = color_data)
            dset = f.create_dataset(INFRARED, data = infrared_data)
            dset = f.create_dataset(FRAMEN, data = infrared_data)
  
        f.close() # close the file
   
    def read_h5py_file(self, filename):
        """
        reads the hp5y file, For testing
        
        Parameters:
        ----------
        filename : string
            file path

        """
        with h5py.File(filename, "r") as f:
            # List all groups
            print("Keys: %s" % f.keys())
            a_group_key = list(f.keys())[0]

            # Get the data
            data = list(f[a_group_key])


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
            
    def show_live_plotting_test(self, N = -1, dt = 1):
        """
        Shows live plotting of the gyro and accel data for testing purposes
        """
        plt.ion()
        fig = plt.figure(figsize = (4,6))
        while self.run:
            gyro_data = self.buffers[GYRO].get_all()
            accel_data = self.buffers[ACCEL].get_all()
            for i in range(3):
                plt.subplot(611 + i)
                plt.plot(gyro_data[:,0]-gyro_data[-1,0],gyro_data[:,i+2])
                plt.xlim([-10,0])
                axes = 'xyz'
                plt.title(f'gyro: axis = {axes[i]}')

            for i in range(3):
                plt.subplot(614 + i)
                plt.plot(accel_data[:,0]-accel_data[-1,0],accel_data[:,i+2])
                plt.xlim([-10,0])
                axes = 'xyz'
                plt.title(f'accel: axis = {axes[i]}')
            fig.tight_layout()
            plt.pause(0.001)
            plt.draw()
            sleep(dt)
            plt.clf()

    def collect_data(self,time):
        """
        Higher order function to collect data
        
        Parameters
        ----------
        time : int
            time to colllect data
        """
        self.start() # starts the threads
       
        for i in range(time):
            sleep(.025)
        self.stop() # orderely stops the piplines
        
        self.save_h5py_file(self.h5py_filename) # saves the data into h5py file
        self.read_h5py_file(self.h5py_filename) # reads the data

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
    from matplotlib import pyplot as plt
    plt.ion()
    device = Device(config_filename = r"intel_realsense_devices\test_files\config_template.conf", h5py_filename = r"intel_realsense_devices\test_files\test.h5py")
    device.init()
    device.start()

    # device.show_live_plotting_test(dt = 1)
    device.collect_data(3)

    # depth_image = device.buffers[DEPTH].get_last_value()
    # print(device.buffers[DEPTH])
    # plt.figure()
    # plt.imshow(depth_image)

