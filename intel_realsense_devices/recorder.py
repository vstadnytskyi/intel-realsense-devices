import h5py
import cv2
from time import sleep
from matplotlib import pyplot as plt
from zmq import device
from intel_realsense_devices.helper import colorize
plt.ion() #interactive on - turns on interactive mode for matplotlib plots. Otherwise you need to have plt.show() command

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
        self.h5py_filename = h5py_filename
        from intel_realsense_devices.device import Device
        self.device = Device(config_filename)
        self.device.init()
        self.driver = self.device.driver
        self.run = None


    def start(self):
        """
        Start the threads to collect and live stream data
        """
        from ubcs_auxiliary.multithreading import new_thread
        threads = {}
        self.device.start()
        threads["record"] = new_thread(self.record)
        self.cv2_live_stream()

    def stop(self):
        self.device.stop() #shut down the device and stop the piplines
        self.save_h5py_file() # saves the data into h5py file
        self.read_h5py_file() # reads the data       


    def record(self):
        """
        Higher order function to collect data and save it to a h5py file
        
        Parameters
        ----------
        None
        """
        last_frame = 0 
        buffer_length = self.device.buffers[FRAMEN].get_all().shape[0] # gets the number of frames
        self.run = True
            
        while last_frame < buffer_length:
            last_frame = self.device.buffers[FRAMEN].get_last_value()[0]
            sleep(0.01)

        self.run = False # shut down the live stream

    def plt_live_stream(self):
        """
        live stream of images using matplotlib 
        """
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
        print("live stream ended")

    def stream_buffer(self):
        """
        stream data in the buffer as a replay
        """
        sleep(3)
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

    def cv2_live_stream(self):
        """
        Live stream images using the cv2 lib
        """
        sleep(1)

        while self.run:
            
            frames = self.device.buffers[FRAMEN].get_last_value()[0]
            # print(f"CV2_live_stream at frame  {frames}")

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

    def live_stream(self):
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

    def show_live_plotting(self, N = -1, dt = 1):
        """
        shows live plotting of the gyro and accel data
        """
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

    def save_h5py_file(self):
        """
        saves the data from the buffers into h5py file
        Parameters
        ----------
        None
        
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
        with h5py.File(self.h5py_filename, 'w') as f:
            dset = f.create_dataset(GYRO, data = gyro_data)
            dset = f.create_dataset(ACCEL, data = accel_data)
            dset = f.create_dataset(DEPTH, data = depth_data)
            dset = f.create_dataset(COLOR, data = color_data)
            dset = f.create_dataset(INFRARED, data = infrared_data)
            dset = f.create_dataset(FRAMEN, data = frameN_data)
  
        f.close() # close the file
   
    def read_h5py_file(self):
        """
        reads the hp5y file data sets, For testing
        
        Parameters:
        ----------
        None

        """
        with h5py.File(self.h5py_filename, "r") as f:
            # List all groups
            print("Keys: %s" % f.keys())
            a_group_key = list(f.keys())[0]


# import sys
# config_filename = (sys.argv[1])
# h5py_filename =  (sys.argv[2])

# config_filename = "test_files\config_L151_f1320305.yaml"
# h5py_filename = "test_files\test.h5py"

# recorder = Recorder(config_filename, h5py_filename)
# recorder.start()

# print(f'Frame array {recorder.device.buffers[FRAMEN].get_all()}')
# recorder.live_stream()

if __name__ == "__main__":
    config_filename = "test_files\config_L151_f1320305.yaml"
    h5py_filename = r"test_files\test2.h5py"

    recorder = Recorder(config_filename, h5py_filename)
    
    recorder.start()
    recorder.save_h5py_file()
    recorder.stop()
