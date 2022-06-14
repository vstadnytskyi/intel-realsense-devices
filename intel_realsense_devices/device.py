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



class Device():
    """ 
    """

    def __init__(self):
        """
        """
        threads = {}
        # Create a context object. This object owns the handles to all connected realsense devices

    def init(self, configuration):
        """
        import intel real sense driver and initializes the device.

        Circular buffers are:
        - depth_image
        - depth_image_timestamp

        """
        from intel_realsense_devices.driver import Driver
        driver = Driver()
        depth_image_shape = driver.get_depth_image_shape()
        depth_image_dtype = driver.get_depth_image_dtype()


        from circular_buffer_numpy.circular_buffer import CircularBuffer
        buffers = {}
        buffers['depth'] = CircularBuffer(shape = (100,)+depth_image_shape, dtype = depth_image_dtype)

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
        threads = {}

    def stop(self):
        """
        orderly stop of device operation
        """
        pass
        
    def run_once_images(self):
        """
        acquires one set of images and saves them in separate circular buffes.
        """
        pass
    
    def run_once_gyroscope(self):
        """
        acquires one set of gyroscope reading and saves them in gyroscope related circular buffer.
        """
        pass

    def run_once_accelerometer(self):
        """
        acquires one set of gyroscope reading and saves them in gyroscope related circular buffer.
        """
        pass

if __name__ is "__main__":
    from matplotlib import pyplot as plt
    plt.ion()
    from intel_realsense_devices.device import Device
    device = Device()
    device.start()
    depth_image = device.buffers['depth'].get_last_value()
    plt.figure()
    plt.imshow(depth_image)

    
