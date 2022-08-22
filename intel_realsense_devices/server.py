#!/usr/bin/env python
"""
    CPU = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = '%')

    MEMORY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = 'GB')

    BATTERY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = '%')

    TIME = pvproperty(value='time unknown', read_only = True, dtype = str)

    dt = pvproperty(value=1.0, precision = 3, units = 's')


"""
import os
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = str(1920*1080*3*20)

from pcaspy import SimpleServer, Driver
import random
from numpy import nan, zeros, int16, random
COLOR = 'color'
DEPTH = 'depth'

width  = {}
height  = {}
width[COLOR] = 960
height[COLOR] = 540
width[DEPTH] = 640
height[COLOR] = 480

prefix = 'L515:'
pvdb = {
    'color' : {
        'prec' : 1,
        'count': width[COLOR]*height[COLOR]*3,
    },
    'depth' : {
        'prec' : 1,
        'count': width[DEPTH]*height[DEPTH],
    },
    'frameN' : {
        'value': 0,
        'prec' : 0,
        'scan' : .1,
        'count': 1,
        'unit': 's' 
    },
    'dt' : {
        'value': 1.0,
        'prec' : 1,
        'scan' : .1,
        'count': 1,
        'unit': 's' 
    },
}


class myDriver(Driver):
    def __init__(self):
        super(myDriver, self).__init__()
        self.width = width
        self.height = height
        from time import time
        self.t_start = time()
        import threading
        threading.Thread(target=self.poll, daemon=True).start()
        self.io_push_queue = None

    def poll(self):
        from time import ctime, time, sleep
        import psutil
        while True:
            if self.io_push_queue is not None:
                data = self.io_push_queue.get()
                for key, value in data.items():
                    self.setParam(key, value)
                self.updatePVs()


    def read(self, reason):
        from time import ctime, time
        import psutil
        if reason == 'image':
            value = self.getParam('image')
        elif reason == 'dt':
            value = self.getParam('dt')
        
        return value

    def write(self, reason, value):
        from time import ctime, time
        import psutil
        import numpy as np
        if reason == 'dt':
            self.setParam(reason,value)
        elif reason == 'image':
            self.setParam(reason,value)

if __name__ == '__main__':
    from time import sleep,ctime, time
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()
    while True:
        server.process(.1)