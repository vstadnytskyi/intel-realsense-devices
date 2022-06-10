# D435i camera test 
import pyrealsense2 as rs
import numpy as np
import time
from PIL import Image as im
import subprocess
def initialize_camera():
    ctx = rs.context()
    devices = ctx.query_devices()
    for device in devices:
        print(' ----- Available devices ----- ')
        print('  Device PID: ',  device.get_info(rs.camera_info.product_id))
        print('  Device name: ',  device.get_info(rs.camera_info.name))
        print('  Serial number: ',  device.get_info(rs.camera_info.serial_number))
        print('  Firmware version: ',  device.get_info(rs.camera_info.firmware_version))
        print('  USB: ',  device.get_info(rs.camera_info.usb_type_descriptor))
        serial=device.get_info(rs.camera_info.serial_number)
        if serial == '139522074713':
            dev = device
        else:
            print('device not found')
 
    serial=dev.get_info(rs.camera_info.serial_number)
    # start the frames pipe
    pipeline = {}
    pipeline['accel'] = rs.pipeline()
    pipeline['gyro'] = rs.pipeline()
    
    conf = {}
    conf['accel'] = rs.config()
    conf['gyro'] = rs.config()

    conf['accel'] .enable_stream(rs.stream.accel)#, rs.format.motion_xyz32f, 250)
    conf['gyro'].enable_stream(rs.stream.gyro)#, rs.format.motion_xyz32f, 200)
    
    conf['gyro'].enable_device(serial)   #test of enable device
    
    profile = {}
    profile['accel'] = pipeline['accel'].start(conf['accel'])
    profile['gyro'] = pipeline['gyro'].start(conf['gyro'])
    

    print ('camera init complete')
    time.sleep(2)
    return pipeline, profile
pipeline,profile = initialize_camera()
for key in profile.keys():
    print(f'profile {key}')
    stream_list = profile[key].get_streams()
    for i in stream_list:
        print(f'stream {i}')
try:
    f = pipeline['gyro'].wait_for_frames()
    accel = (f[0].as_motion_frame().get_motion_data())
    gyro =  (f[0].as_motion_frame().get_motion_data())
    print('--- --- --- --- --- ---')
    print("accelerometer: ", accel)
    print('accelerometer frame #: ',f[0].get_frame_number())
    print("gyro: ", gyro)
    print('gyro frame #: ',f[0].get_frame_number())
finally:
    pass #p.stop()

def run_get_gyro_once(pipeline,profile):
    from time import time
    key = 'gyro'
    f = pipeline[key].wait_for_frames()
    gyro = (f[0].as_motion_frame().get_motion_data())
    frameN = f[0].as_motion_frame().frame_number
    t = time()
    gyro_array = np.asanyarray((t,frameN,gyro.x,gyro.y,gyro.z)).reshape(1,5)
    buffers['gyro'].append(gyro_array)

def run_get_accel_once(pipeline,profile):
    from time import time
    key = 'accel'
    f = pipeline[key].wait_for_frames()
    accel = (f[0].as_motion_frame().get_motion_data())
    frameN = f[0].as_motion_frame().frame_number
    t = time()
    accel_array = np.asanyarray((t,frameN,accel.x,accel.y,accel.z)).reshape(1,5)

    buffers['accel'].append(accel_array)

def run_get_gyro(pipeline,profile):
    while True:
        run_get_gyro_once(pipeline = pipeline, profile = profile)
        
def run_get_accel(pipeline,profile):
    while True:
        run_get_accel_once(pipeline = pipeline, profile = profile)
        
from circular_buffer_numpy.circular_buffer import CircularBuffer
buffers = {}
buffers['gyro'] = CircularBuffer((30000,5), dtype = 'float64')
buffers['accel'] = CircularBuffer((30000,5), dtype = 'float64')

from ubcs_auxiliary.threading import new_thread
threads = {}
threads['gyro'] = new_thread(run_get_gyro,pipeline = pipeline,profile = profile)
threads['accel'] = new_thread(run_get_accel,pipeline = pipeline,profile = profile)

%matplotlib inline
from time import time, sleep
import pylab
from matplotlib import pyplot as plt
from IPython import display
def show_live_plotting(N = -1, dt = 1):
    fig = plt.figure(figsize = (18,24))
    while True:
        plt.clf()
        gyro_data = buffers['gyro'].get_all()
        accel_data = buffers['accel'].get_all()
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
        display.display(pylab.gcf())
        display.clear_output(wait=True)
        sleep(dt)

show_live_plotting(dt = 1)



