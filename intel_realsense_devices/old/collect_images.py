from matplotlib import pyplot as plt
import numpy as np 
import time
import pyrealsense2 as rs
from pdb import pm

class Collect_Images():
    
    def __init__(self):
        from device import Device



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
    pass
