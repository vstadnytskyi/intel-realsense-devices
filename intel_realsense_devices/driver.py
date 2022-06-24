"""
Driver for intel realsense devices. This file contains simple wrappers for functions provided by Intel SDK.
https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples
https://dev.intelrealsense.com/docs/python2

some names of variables and functions come Intel SDK

Currently supports:
Intel LiDAR L515
Intel Depth Camera D435i
"""

from tkinter import Image
from tkinter.tix import IMAGE
from typing_extensions import Self
from matplotlib import image
import numpy as np 
import time
import pyrealsense2 as rs
from pdb import pm



DEPTH = "depth"
COLOR = "color"
INFRARED = "infrared"
GYRO = "gyro"
ACCEL = "accel"
IMAGES = "images"
class Driver():
    """ 
    """

    def __init__(self):
        """
        """
        self.pipeline = {}
        self.profile = {}
        self.conf = {}
        # Create a context object. This object owns the handles to all connected realsense devices

    def init(self,serial_number = ''):
        """
        Method for Initalizing classe
        """
        # creates the piplines
        self.pipeline[ACCEL] = rs.pipeline()
        self.pipeline[GYRO] = rs.pipeline()
        self.pipeline[IMAGE] = rs.pipeline()
        
        # setup the configuration for each frame type
        self.conf[ACCEL] = rs.config()
        self.conf[GYRO] = rs.config()
        self.conf[IMAGE] = rs.config()
        
        # sets up the device 
        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline[IMAGE])
        self.pipeline_profile = self.conf[IMAGE].resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        
        self.print_device_info() 
        self.configure() # calls method to configure the device

        self.conf[IMAGE].enable_device(serial_number)
        self.conf[GYRO].enable_device(serial_number)

        self.start()

    def print_device_info(self):
        """
        Prints the device information
        Parameter : Nothing
        Returns: Nothings
        """
        print(' ----- Available devices ----- ')
        print('  Device PID: ',  self.device.get_info(rs.camera_info.product_id))
        print('  Device name: ',  self.device.get_info(rs.camera_info.name))
        print('  Serial number: ',  self.device.get_info(rs.camera_info.serial_number))
        print('  Firmware version: ',  self.device.get_info(rs.camera_info.firmware_version))
        print('  USB: ',  self.device.get_info(rs.camera_info.usb_type_descriptor))

    def start(self):
        """
        starts the pipelines
        """
        self.profile[ACCEL] = self.pipeline[ACCEL].start(self.conf[ACCEL])
        self.profile[GYRO] = self.pipeline[GYRO].start(self.conf[GYRO])
        self.profile[IMAGE] = self.pipeline[IMAGE].start(self.conf[IMAGE])

    def stop(self):
        """
        stops the pipelines
        """
        self.profile[ACCEL] = self.pipeline[ACCEL].stop(self.conf[ACCEL])
        self.profile[GYRO] = self.pipeline[GYRO].stop(self.conf[GYRO])
        self.profile[IMAGE] = self.pipeline[IMAGE].stop(self.conf[IMAGE])
        
    def find_devices(self):
        """
        returns a list of all connected intel realsense devices
        """
        context = rs.context()
        connect_device = []

        for d in context.devices:
            if d.get_info(rs.camera_info.name).lower() != 'platform camera':
                serial = d.get_info(rs.camera_info.serial_number)
                product_line = d.get_info(rs.camera_info.product_line)
                device_info = (serial, product_line) # (serial_number, product_line)
                connect_device.append( device_info )
        return connect_device

    def configure(self):
        """
        Enablles the stream for all configurations of the camera 
        """
        device_serial_number = str(self.device.get_info(rs.camera_info.serial_number))
        device_product_line = str(self.device.get_info(rs.camera_info.product_line))
        self.conf[IMAGE].enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        if device_product_line == 'L500':
            self.conf[IMAGE].enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            self.conf[IMAGE].enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        try:
            self.conf[ACCEL].enable_stream(rs.stream.accel)#,rs.format.motion_xyz32f,200)
            self.conf[GYRO].enable_stream(rs.stream.gyro)#,rs.format.motion_xyz32f,200)
            self.conf[IMAGE].enable_stream(rs.stream.infrared)
            self.conf[IMAGE].enable_stream(rs.stream.depth)
            print("Enabled all streams ")
            
        except Exception as e:
            print('during IMU configuratuon the following error occured',e)


    def get_data(self):
        import numpy as np
        frames = self.pipeline[IMAGE].wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        try:
            imu = frames[2].as_motion_frame().get_motion_data()
            imu1 = (imu.x,imu.y,imu.z)
            imu = frames[3].as_motion_frame().get_motion_data()
            imu2 = (imu.x,imu.y,imu.z)
        except:
            imu1 = (np.nan,np.nan,np.nan)
            imu2 = (np.nan,np.nan,np.nan)
        frameN = frames.get_frame_number()
        # Convert images to numpy arrays
        # it is important to copy the array. 
        #Otherwise it stops returning new frames after 15 images.
        depth_image = np.copy(np.asanyarray(depth_frame.get_data()))
        color_image = np.copy(np.asanyarray(color_frame.get_data()))
        return {'depth':depth_image,'color': color_image,'imu1':imu1,'imu2':imu2,'frame#':frameN}
        

    def get_depth_resolution(self):
        """
        returns depth resolution of the camera in meters per count
        """
        result = self.device.first_depth_sensor().get_depth_scale()
        return result
    
    depth_resolution = property(get_depth_resolution)
    
    def get_all_available_options(self):
        """
        an auxiliary function to retrieve all available options for a given model
        """
        pipeline_profile = self.pipeline_profile
        dev = pipeline_profile.get_device()
        depth_sensor = None
        for sensor in dev.query_sensors():
            if sensor.is_depth_sensor():
                depth_sensor = dev.query_sensors()[0]
        for option in depth_sensor.get_supported_options():
            print('---',option,'---')
            print('description:',depth_sensor.get_option_description(option))
            print('currennt value:',depth_sensor.get_option(option))

    def set_laser_intensity(self, laser_power):
        """
        Sets laser intensity for L515 depth camera  
        Paramter: takes in laser power intensity
        Returns: nothing
        """

        if laser_power < 0 or laser_power > 100 :
            print("Laser power must be between 0- 100")
            return

        for frame_type in self.profile.keys():
            dev = self.profile[frame_type].get_device()
            depth_sensor = dev.query_sensors()[0]
            depth_sensor.set_option(rs.option.laser_power, laser_power)
    
    def get_images(self):
        """
        Setting up a dict containing images that are recived from the pipline
        Parameters: Nothing
        Returns: Dict containing images  
        """

        f = self.pipeline[IMAGE].wait_for_frames()

        color = f.get_color_frame()
        infrared = f.get_infrared_frame()
        depth = f.get_depth_frame()

        color_img = np.asanyarray(color.get_data())
        ir_img = np.asanyarray(infrared.get_data())
        depth_img = np.asanyarray(depth.get_data())

        return {"color": color_img, "depth" : depth_img, "infrared" : ir_img}
        
    def get_image_dtype(self, frame_type):
        """ 
        returns the image data type
        Parameter: Nothing
        Returns: image data type
        """
        return self.get_images()[frame_type].dtype

    def get_image_shape(self, frame_type):
        """ 
        returns the image Shape
        Parameter: Nothing
        Returns: image Shape size 
        """
        return self.get_images()[frame_type].shape
    
    def live_stream_test(self):
        """
        Test that plays a live stream of depth color and infared for about 10 seconds
        """
        plt.ion() #interactive on - turns on interactive mode for matplotlib plots. Otherwise you need to have plt.show() command

        for i in range(10):
            plt.pause(.0001)
            plt.subplot(131)
            plt.imshow(self.get_images()['depth'])

            plt.title('Live depth')

            plt.subplot(132)
            plt.imshow(self.get_images()['color'])
            plt.title('Live color')

            plt.subplot(133)
            plt.imshow(self.get_images()['infrared'])
            plt.title('Live infrared') 
            time.sleep(1)

if __name__ == "__main__":
    from matplotlib import pyplot as plt
    #plt.ion()
    driver = Driver()
    driver.init(serial_number = 'f1320305')
    #driver.print_device_info()
    #plt.imshow(driver.get_images()['depth'])
    plt.pause(.02)
    plt.show()
    driver.set_laser_intensity(10)
    driver.live_stream_test()