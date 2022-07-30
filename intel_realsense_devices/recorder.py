from time import time, sleep
import h5py

DEPTH = "depth"
COLOR = "color"
INFRARED = "infrared"
GYRO = "gyro"
ACCEL = "accel"
IMAGE = "image"
FRAMEN = "frameN"

class Recorder():
    """
    Higher order class to collect data from device.
    """
    
    def __init__(self, config_filename, h5py_filename):
        """
        Initializes the the device class

        Parameters:
        ------------
        config_filename: string
            config file path

        h5py_filename: string
            h5py file path
        """
        from intel_realsense_devices.device import Device
        self.device = Device(config_filename)
        # self.driver = self.device.driver
        self.device.init()

        self.h5py_filename = h5py_filename

    def record(self):
        """
        Higher order function to collect data
        
        Parameters
        ----------
        time : int
            time to colllect data
        """

        self.device.start() # starts the threads
        last_frame = 0
        buffer_length = self.device.buffers[FRAMEN].get_all().shape[0]

        while last_frame < buffer_length:
            last_frame = self.device.buffers[FRAMEN].get_last_value()[0]
        
        self.device.stop() # shuts down the threads and piplines
        
        self.save_h5py_file(self.h5py_filename) # saves the data into h5py file
        self.read_h5py_file(self.h5py_filename) # reads the data

    def save_h5py_file(self, filename):
        """
        saves the data from the buffers into h5py file
        Parameters
        ----------
        filename : string 
            path to H5py file
        
        """
        buffers = self.device.buffers
        # grab all the data in the circular buffer
        gyro_data = buffers[GYRO].get_all()
        accel_data = buffers[ACCEL].get_all()
        depth_data = buffers[DEPTH].get_all()
        infrared_data = buffers[INFRARED].get_all()
        color_data = buffers[COLOR].get_all()
        frameN_data = buffers[FRAMEN].get_all()

        # write data in the H5PY file
        with h5py.File(filename, 'w') as f:
            dset = f.create_dataset(GYRO, data = gyro_data)
            dset = f.create_dataset(ACCEL, data = accel_data)
            dset = f.create_dataset(DEPTH, data = depth_data)
            dset = f.create_dataset(COLOR, data = color_data)
            dset = f.create_dataset(INFRARED, data = infrared_data)
            dset = f.create_dataset(FRAMEN, data = frameN_data)
  
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

    def live_stream_test(self):
        """
        Test that plays a live stream of depth color and infared for about 10 seconds
        """
        from matplotlib import pyplot as plt
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

    def show_live_plotting(self, N = -1, dt = 1):
        """
        shows live plotting of the gyro and accel data
        """
        from matplotlib import pyplot as plt
        plt.ion()
        self.device.start()
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
        self.device.stop()
    

import sys
config_filename = (sys.argv[1])
h5py_filename =  (sys.argv[2])
recorder = Recorder(config_filename, h5py_filename)
recorder.record()
