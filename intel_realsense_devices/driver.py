"""
Driver for intel realsense devices. This file contains simple wrappers for functions provided by Intel SDK.
https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples
https://dev.intelrealsense.com/docs/python2

some names of variables and functions come Intel SDK

Currently supports:
Intel LiDAR L515
Intel Depth Camera D435i
"""

import numpy as np 
from time import time, ctime, sleep


class Driver():
    """
    """

    def __init__(self):
        """
        """
        pass
        # Create a context object. This object owns the handles to all connected realsense devices

    def init(self,serial_number = ''):
        import pyrealsense2 as rs
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_device(serial_number)
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.configure()
        self.pipeline.start(self.config)

    self.start(self):
        self.pipeline.start(self.config)

    def stop(self):
        self.pipeline.stop()
        
    def find_devices(self):
        """
        returns a list of all connected intel realsense devices
        """
        import pyrealsense2 as rs
        context = rs.context()
        connect_device = []

        for d in context.devices:
            if d.get_info(rs.camera_info.name).lower() != 'platform camera':
                serial = d.get_info(rs.camera_info.serial_number)
                product_line = d.get_info(rs.camera_info.product_line)
                device_info = (serial, product_line) # (serial_number, product_line)
                connect_device.append( device_info )
        return connect_device


    def enable_device(self,serial_number = ''):
        """
        """
        self.serial_number = serial_number
        # connected_devices = self.find_devices()
        # if len(connected_devices) > 0:
        #     for device in connected_devices:
        #         print(device)
        #         if serial_number == device[0]:
        #             break

        

        print(device)
       
        print(f'serial_number = {serial_number}',device )

    def configure(self):
        import pyrealsense2 as rs
        device_serial_number = str(self.device.get_info(rs.camera_info.serial_number))
        device_product_line = str(self.device.get_info(rs.camera_info.product_line))
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        if device_product_line == 'L500':
            self.config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.config.enable_stream(rs.stream.accel)#,rs.format.motion_xyz32f,200)
        self.config.enable_stream(rs.stream.gyro)#,rs.format.motion_xyz32f,200)

    def get_data(self):
        import numpy as np
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        imu = frames[2].as_motion_frame().get_motion_data()
        imu1 = (imu.x,imu.y,imu.z)
        imu = frames[3].as_motion_frame().get_motion_data()
        imu2 = (imu.x,imu.y,imu.z)
        frameN = frames.get_frame_number()
        # Convert images to numpy arrays
        # it is important to copy the array. 
        #Otherwise it stops returning new frames after 15 images.
        depth_image = np.copy(np.asanyarray(depth_frame.get_data()))
        color_image = np.copy(np.asanyarray(color_frame.get_data()))
        return {'depth':depth_image,'color': color_image,'imu1':imu1,'imu2':imu2,'frame#':frameN}
        

    def get_depth_resolution(self):
        """
        returns depth resolution of the camera in mm per count
        In [152]: a = 



        In [154]: self.device.first_depth_sensor().get_depth_scale?
        Docstring:
        get_depth_scale(self: pyrealsense2.pyrealsense2.depth_sensor) -> float

        Retrieves mapping between the units of the depth image and meters.
        Type:      method

        In [153]: a.get_depth_scale()
        Out[153]: 0.0002500000118743628

        """
        result = self.device.first_depth_sensor().get_depth_scale
        return result
    depth_resolution = property(get_depth_resolution)
    



if __name__ is "__main__":
    from matplotlib import pyplot as plt
    plt.ion()
    driver = Driver()
    print("driver.init(serial_number = '139522074713')")
    print("plt.imshow(driver.get_images()['depth'])")
    