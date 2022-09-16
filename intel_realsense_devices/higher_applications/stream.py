
import h5py
import cv2
from time import sleep
from matplotlib import pyplot as plt

from intel_realsense_devices.helper import colorize
plt.ion() #interactive on - turns on interactive mode for matplotlib plots. Otherwise you need to have plt.show() command

DEPTH = "depth"
COLOR = "color"
INFRARED = "infrared"
GYRO = "gyro"
ACCEL = "accel"
IMAGE = "image"
FRAMEN = "frameN"

class Stream():
    "Higher level application that can stream live data from the camera"

    def __init__(self, config_filename):
        from intel_realsense_devices.device import Device
        self.device = Device(config_filename)
        self.device.init()
        self.driver = self.device.driver
        self.run = True
        
    def plt_live_stream(self):
        """
        live stream of images using matplotlib 
        """

        self.device.start()

        while self.run:

            plt.pause(.0001)
            plt.subplot(131)
            d = self.device.buffers[DEPTH].get_last_value()
            depth = d[0,:,:]
            plt.imshow(depth)

            plt.title('Live depth')

            plt.subplot(132)
            c = self.device.buffers[COLOR].get_last_value()
            color = c[0,:,:, :]
            plt.imshow(color)

            plt.title('Live color')

            plt.subplot(133)
            i = self.device.buffers[INFRARED].get_last_value()
            infrared = i[0,:,:]
            plt.imshow(infrared)
            plt.title('Live infrared') 
            sleep(0.25)

    def stream_buffer(self):
        """
        stream data in the buffer as a replay
        """
        self.device.start()

        buffer_length = self.device.buffers[FRAMEN].get_all().shape[0] 

        d = self.device.buffers[DEPTH].get_all()
        c = self.device.buffers[COLOR].get_all()
        inf = self.device.buffers[INFRARED].get_all()

        for i in range(buffer_length):
            
            color = c[i]
            depth = d[i]
            infrared = inf[i]
            
            if depth is not None:
                cv2.imshow("Depth", colorize(depth, (None, 5000)))
            if infrared is not None:
                cv2.imshow("IR", colorize(infrared, (None, 500), colormap=cv2.COLORMAP_JET))
            if color is not None:
                cv2.imshow("Color", color)

            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                self.run = False

    def cv2_live_stream_buffer(self):
        """
        Live stream images using the cv2 lib.
        Used while collecting data.
        """
        
        self.device.start()

        while self.run:
            
            frames = self.device.buffers[FRAMEN].get_last_value()[0]

            d = self.device.buffers[DEPTH].get_last_value()
            depth = d[0,:,:]
            c = self.device.buffers[COLOR].get_last_value()
            color = c[0,:,:, :]
            i = self.device.buffers[INFRARED].get_last_value()
            ir = i[0,:,:]

            if depth is not None:
                cv2.imshow("Depth", colorize(depth, (None, 5000)))
            if ir is not None:
                cv2.imshow("IR", colorize(ir, (None, 500), colormap=cv2.COLORMAP_JET))
            if color is not None:
                cv2.imshow("Color", color)
            
            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                self.run = False

        cv2.destroyAllWindows()

    def Cv2_live_stream(self):
        """
        Stream live images from the camera
        """
        self.device.start()

        while True:
            dict = self.device.driver.get_images()

            color = dict[COLOR]
            depth = dict[DEPTH]
            infrared = dict[INFRARED]
            
            if depth is not None:
                cv2.imshow("Depth", colorize(depth, (None, 5000)))
            if infrared is not None:
                cv2.imshow("IR", colorize(infrared, (None, 500), colormap=cv2.COLORMAP_JET))
            if color is not None:
                cv2.imshow("Color", color)

            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                self.run = False

    def IMU_live_plotting(self, N = -1, dt = 1):
        """
        shows live plotting of the gyro and accel data
        """
        self.device.start()

        from matplotlib import pyplot as plt
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
        self.device.stop()


if __name__ == "__main__":
    config_filename = "test_files\config_L515_f1231322.yaml"
    stream = Stream(config_filename)
    stream.IMU_live_plotting()

