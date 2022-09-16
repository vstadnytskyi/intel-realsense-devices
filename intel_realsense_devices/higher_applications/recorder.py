import tempfile
import h5py
import cv2

from time import sleep

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
        self.config_filename = config_filename
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

        from intel_realsense_devices.higher_applications.stream import Stream

        stream = Stream(self.config_filename)
        stream.cv2_live_stream()

    def stop(self):
        """ 
        orderly shutdown of the pipelines in the driver class.
        """
        self.device.stop() #shut down the device and stop the piplines
        self.device.driver.stop()
    
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
            dset = f.create_dataset(COLOR, data = color_data)
            dset = f.create_dataset(INFRARED, data = infrared_data)
            dset = f.create_dataset(DEPTH, data = depth_data)
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


if __name__ == "__main__":
    import os
    import sys
    import logging
    from logging import debug, info, warning, error

    logging.getLogger("blib2to3").setLevel(logging.ERROR)
    logging.getLogger("parso").setLevel(logging.ERROR)
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    logging.getLogger("PIL").setLevel(logging.ERROR)
    logging.getLogger("asyncio").setLevel(logging.ERROR)
    

    if len(sys.argv) > 1:
        debug('reading specified config file and h5py file as arg')
        config_filename = (sys.argv[1])
        h5py_filename =  (sys.argv[2])
        info(config_filename, " " , h5py_filename)

    else:
        debug('reading specified config file and h5py file from user')
        # config_filename = r"test_files\config_L151_f1320305.yaml"
        config_filename = "test_files\config_L515_f1231322.yaml"
        h5py_filename = r"test_files\test.h5py"
        info(config_filename, " " , h5py_filename)

    recorder = Recorder(config_filename, h5py_filename)

    recorder.start() 
    recorder.save_h5py_file()
    recorder.stop()

