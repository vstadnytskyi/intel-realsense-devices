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
import pyrealsense2 as rs

DEPTH = "depth"
COLOR = "color"
INFRARED = "infrared"
GYRO = "gyro"
ACCEL = "accel"
IMAGES = "images"


class Device():
    """ 
    """

    def __init__(self):
        """
        """
        # where should the buffer, threads be init
        
        # Create a context object. This object owns the handles to all connected realsense devices

    def init(self):
        """
        import intel real sense driver and initializes the device.

        Circular buffers are:
        - depth_image
        - depth_image_timestamp

        """
        from driver import Driver
        self.driver = Driver()
        self.driver.init(serial_number = 'f1320305')
        
        self.threads = {}
        self.buffers = {}
        self.profile = {}
    
        self.pipeline = {}
        self.pipeline['accel'] = rs.pipeline()
        self.pipeline['gyro'] = rs.pipeline()
        
        self.conf = {}
        self.conf['accel'] = rs.config()
        self.conf['gyro'] = rs.config()

        self.conf['accel'].enable_stream(rs.stream.accel)#, rs.format.motion_xyz32f, 250)
        self.conf['gyro'].enable_stream(rs.stream.gyro)#, rs.format.motion_xyz32f, 200)
        
        self.profile = {}
        self.profile['accel'] = self.pipeline['accel'].start(self.conf['accel'])
        self.profile['gyro'] = self.pipeline['gyro'].start(self.conf['gyro'])
        
        # intialialize the circular buffer
        from circular_buffer_numpy.circular_buffer import CircularBuffer
        self.buffers['depth'] = CircularBuffer(shape = (100,)+ self.driver.get_image_shape("depth"), dtype = self.driver.get_image_dtype("depth")) 
        self.buffers['color'] = CircularBuffer(shape = (100,)+ self.driver.get_image_shape("color"), dtype = self.driver.get_image_dtype("color")) 
        self.buffers['infrared'] = CircularBuffer(shape = (100,)+ self.driver.get_image_shape("infrared"), dtype = self.driver.get_image_dtype("infrared")) 
        self.buffers['gyro'] = CircularBuffer((30000,5), dtype = 'float64')
        self.buffers['accel'] = CircularBuffer((30000,5), dtype = 'float64')
        

        
    def read_config_file(self, filename):
        """reads configuration file and returns dictionary of parameters. The configuration file is created using YAML.

        Parameters
        ----------
        filename : string
            path to configuration file

        Returns
        -------
        dictionary
            dictionary with configuration parameters.

        """
        import yamp
        self.config_filename = filename
        #read yaml file and return dictionary
        pass

    def start(self):
        """
        orderly start of device operation
        """
        from ubcs_auxiliary.multithreading import new_thread
        
        self.threads[GYRO] = new_thread(self.run_get_gyro)
        self.threads[ACCEL] = new_thread(self.run_get_accel)
        self.threads[IMAGES] = new_thread(self.run_once_images)

    def stop(self):
        """
        orderly stop of device operation
        """
        pass
        
    def run_once_images(self):
        """
        acquires one set of images and saves them in separate circular buffes.
        """
        
        self.buffers[DEPTH] = self.driver.get_images()[DEPTH]
        self.buffers[COLOR] = self.driver.get_images()[COLOR]
        self.buffers[INFRARED] = self.driver.get_images()[INFRARED]
            
    def run_once_gyroscope(self):
        """
        acquires one set of gyroscope reading and saves them in gyroscope related circular buffer.
        """

        f = self.driver.pipeline.wait_for_frames()
        gyro = (f[0].as_motion_frame().get_motion_data())
        frameN = f[0].as_motion_frame().frame_number
        t = time()
        gyro_array = np.asanyarray((t,frameN,gyro.x,gyro.y,gyro.z)).reshape(1,5)
        self.buffers[GYRO].append(gyro_array)

    def run_once_accelerometer(self):
        """
        acquires one set of gyroscope reading and saves them in gyroscope related circular buffer.
        """

        f = self.pipeline[ACCEL].wait_for_frames()
        accel = (f[0].as_motion_frame().get_motion_data())
        frameN = f[0].as_motion_frame().frame_number
        t = time()
        accel_array = np.asanyarray((t,frameN,accel.x,accel.y,accel.z)).reshape(1,5)
        self.buffers[ACCEL].append(accel_array)

    def run_get_gyro(self):
        while True:
            self.run_once_gyroscope()
            
    def run_get_accel(self):
        while True:
            self.run_once_accelerometer()

    def show_live_plotting(self, N = -1, dt = 1):
        plt.ion()
        fig = plt.figure(figsize = (4,6))
        while True:
            gyro_data = self.buffers['gyro'].get_all()
            accel_data = self.buffers['accel'].get_all()
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

if __name__ == "__main__":
    from matplotlib import pyplot as plt
    plt.ion()
    #from intel_realsense_devices.driver import Driver
    device = Device()
    device.init()
    device.start()
    device.show_live_plotting(dt = 1)
    # depth_image = device.buffers[DEPTH].get_last_value()
    
    # print(device.buffers[DEPTH])
    # plt.figure()
    # plt.imshow(depth_image)


    