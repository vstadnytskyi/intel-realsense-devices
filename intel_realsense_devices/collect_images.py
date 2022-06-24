from matplotlib import pyplot as plt
import numpy as np 
from time import time, sleep
import pyrealsense2 as rs
from pdb import pm

from zmq import device

DEPTH = "depth"
COLOR = "color"
INFRARED = "infrared"
GYRO = "gyro"
ACCEL = "accel"
IMAGE = "image"

class Collect_Images():
    
    def __init__(self, yaml_filename, h5py_filename):
        from device import Device
        self.device = Device(config_filename = yaml_filename, h5py_filename = h5py_filename)
        self.device.init()
        self.driver = self.device.driver

    def live_stream_test(self):
        """
        Test that plays a live stream of depth color and infared for about 10 seconds
        """
        plt.ion() #interactive on - turns on interactive mode for matplotlib plots. Otherwise you need to have plt.show() command

        for i in range(10):
            plt.pause(.0001)
            plt.subplot(131)
            plt.imshow(self.driver.get_images()['depth'])

            plt.title('Live depth')

            plt.subplot(132)
            plt.imshow(self.driver.get_images()['color'])
            plt.title('Live color')

            plt.subplot(133)
            plt.imshow(self.driver.get_images()['infrared'])
            plt.title('Live infrared') 
            sleep(1)
    
    def collect_data(self,time):
        self.device.start()
        for i in range(time):
            sleep(1)
        self.device.stop()

    def show_live_plotting(self, N = -1, dt = 1):
        """
        shows live plotting of the gyro and accel data
        """
        plt.ion()
        fig = plt.figure(figsize = (4,6))
        while self.device.run:
            gyro_data = self.device.buffers[GYRO].get_all()
            accel_data = self.device.buffers[ACCEL].get_all()
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
    collect_images = Collect_Images("config.yaml", "test.h5py")
    collect_images.collect_data(3)

