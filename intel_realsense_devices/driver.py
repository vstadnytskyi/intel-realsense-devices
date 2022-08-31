"""
Driver for intel realsense devices. This file contains simple wrappers for functions provided by Intel SDK.
https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples
https://dev.intelrealsense.com/docs/python2

some names of variables and functions come Intel SDK

Currently supports:
Intel LiDAR L515
Intel Depth Camera D435i
"""


from matplotlib import image
import numpy as np 
import time
import pyrealsense2 as rs


DEPTH = "depth"
COLOR = "color"
INFRARED = "infrared"
GYRO = "gyro"
ACCEL = "accel"
IMAGE = "images"
FRAMEN = "frameN"

DEPTHCHANNEL = 0
COLORCHANNEL = 1
INFARAREDCHANNEL = 2
ACCELCHANNEL = 3
GYROCHANNEL = 4
FPS = "fps"

class Driver():
    """ 
    """

    def __init__(self):
        """
        Create a context object. This object owns the handles to all connected realsense devices
        """
        self.pipeline = {}
        self.profile = {}
        self.conf = {}
        self.config_dict = {}

    def init(self, config_dict):
        """
        Method for Initalizing camera
        """
        from logging import warn, error
        if "serial_number" not in config_dict:
            error(" No serial_number paremter in configuration dictionary")
            return 
        
        serial_number = config_dict["serial_number"]

        # check if SN matches 
        if not self.SN_match(serial_number):
            warn('camera with given serial number is not found')
            return
            
        self.config_dict = config_dict
        
        # creates the piplines
        self.pipeline[ACCEL] = rs.pipeline()
        self.pipeline[GYRO] = rs.pipeline()
        self.pipeline[IMAGE] = rs.pipeline()
    
        # sets up the device 
        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline[IMAGE])
        self.pipeline_profile = self.conf[IMAGE].resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()

        self.print_device_info() 
        self.configure() # calls method to configure the device
        self.start()

    
    def SN_match(self, serial_number):
        """
        returns flag if serial number matches, configures and enables the device
        Parameter : serial number
        Returns: bool 
        """
        from logging import warn, info
        ctx = rs.context()
        devices = ctx.query_devices()
        for device in devices:
            serial = device.get_info(rs.camera_info.serial_number)
            if serial == serial_number:
                info('Device Found')
               
                # setup the configuration for each frame type
                self.conf[ACCEL] = rs.config()
                self.conf[GYRO] = rs.config()
                self.conf[IMAGE] = rs.config()      
                
                #enable device
                self.conf[IMAGE].enable_device(serial_number)
                self.conf[GYRO].enable_device(serial_number)

                return True
        warn('Device not found')
        return False

    def print_device_info(self):
        """
        Prints the device information
        Parameter : Nothing
        Returns: Nothings
        """
        import pyrealsense2 as rs
        from logging import info
        info(' ----- Device ----- ')
        info(f'  Device PID: {self.device.get_info(rs.camera_info.product_id)}')
        info(f'  Device name:  {self.device.get_info(rs.camera_info.name)}')
        info(f'  Serial number:  {self.device.get_info(rs.camera_info.serial_number)}')
        info(f'  Firmware version:   {self.device.get_info(rs.camera_info.firmware_version)}')
        info(f'  USB:  {self.device.get_info(rs.camera_info.usb_type_descriptor)}')

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
        self.profile[ACCEL] = self.pipeline[ACCEL].stop()
        self.profile[GYRO] = self.pipeline[GYRO].stop()
        self.profile[IMAGE] = self.pipeline[IMAGE].stop()
        
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
        from logging import error, warn, info, debug
        device_serial_number = str(self.device.get_info(rs.camera_info.serial_number))
        device_product_line = str(self.device.get_info(rs.camera_info.product_line))
        self.conf[IMAGE].enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        

        if device_product_line == 'L500':
            self.conf[IMAGE].enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            self.conf[IMAGE].enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        
        try:
            self.conf[IMAGE].enable_stream(rs.stream.infrared)
            self.conf[IMAGE].enable_stream(rs.stream.depth)
            info("Enabled color, infared and depth streams ")
            
        except Exception as e:
            error('during image configuratuon the following error occured',e)

        if self.config_dict["channels"] != None:

            try: 
                gyro_fps = self.config_dict["channels"][GYROCHANNEL][FPS]
                accel_fps = self.config_dict["channels"][ACCELCHANNEL][FPS]
                
                self.conf[ACCEL].enable_stream(rs.stream.accel,stream_index = 0,format = rs.format.motion_xyz32f, framerate = accel_fps)
                self.conf[GYRO].enable_stream(rs.stream.gyro,stream_index = 0,format = rs.format.motion_xyz32f, framerate = gyro_fps)

            except Exception as e:
                error('during IMU configuratuon the following error occured',e)

        else:
            try: 
                self.conf[ACCEL].enable_stream(rs.stream.accel)
                self.conf[GYRO].enable_stream(rs.stream.gyro)

            except Exception as e:
                error('during DEFAULT IMU configuratuon the following error occured',e)
    
    def hardware_reset(self):
        """
        resets hardware
        """
        for frame in self.profile.keys():
            dev = self.profile[frame].get_device()
            dev.hardware_reset()

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
        Sets laser intensity for Intel realsense camera  
        Paramter: takes in laser power intensity
        Returns: nothing
        """
        from logging import error,warn,info,debug
        if laser_power < 0 or laser_power > 360 :
            warn("Laser power must be between 0-360")
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
        from logging import error,warn,info,debug
        f = self.pipeline[IMAGE].wait_for_frames()
        
        #collect the frame for each frame type
        frameN = f.get_frame_number()
        color = f.get_color_frame()
        infrared = f.get_infrared_frame()
        depth = f.get_depth_frame()
        # print("frameN", frameN)
        color_img = np.asanyarray(color.get_data())
        ir_img = np.asanyarray(infrared.get_data())
        depth_img = np.asanyarray(depth.get_data())
        FrameN_nparray = np.asanyarray(frameN)
        
        return {COLOR: color_img, DEPTH : depth_img, INFRARED : ir_img , FRAMEN : FrameN_nparray}
        
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
    
if __name__ == "__main__":
    from tempfile import gettempdir
    import logging
    import os
    import yaml

    logging.getLogger("blib2to3").setLevel(logging.ERROR)
    logging.getLogger("parso").setLevel(logging.ERROR)
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    logging.getLogger("PIL").setLevel(logging.ERROR)
    logging.getLogger("asyncio").setLevel(logging.ERROR)
    

    log_filename = os.path.join(gettempdir(),'intel_realsense_driver.log')
    logging.basicConfig(filename=log_filename,
                level=logging.DEBUG,
                format="%(asctime)-15s|PID:%(process)-6s|%(levelname)-8s|%(name)s| module:%(module)s-%(funcName)s|message:%(message)s")

    from matplotlib import pyplot as plt
    #plt.ion()
    driver = Driver()
    # SN = "139522074713"
    # SN = "f1231322"
    # config_filename = r"C:\Users\Abdel Nasser\Documents\L151 Camera\intel-realsense-devices\intel_realsense_devices\test_files\config_d435i__139522074713.yaml"
    config_filename = "test_files\config_L151_f1320305.yaml"
    with open(config_filename) as f:
        config_dict = yaml.safe_load(f)
        driver.init(config_dict)
