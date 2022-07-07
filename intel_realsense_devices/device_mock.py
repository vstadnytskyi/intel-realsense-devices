
class DeviceMock(object):
    def __init__(self):
        io_push_queue = None
        self.frameN = 0
        self.dt = 1

    def io_push(self, dict):
        if self.io_push_queue is not None:
            self.io_push_queue.put(dict)

    def getcwd(self):
        import os
        print(os.getcwd())
        return os.getcwd()

    def get_images(self):
        from ubcs_auxiliary.save_load_object import load_from_file
        import os
        depth = load_from_file(os.path.join(__file__,'../data/1656595569.2276175_depth.npy'))
        color = load_from_file(os.path.join(__file__,'../data/1656595569.2276175_color.npy'))
        self.frameN += 1
        return {'depth':depth, 'color':color, 'frameN':self.frameN}


    def run_once(self):
        images = self.get_images()
        self.io_push(images)

    def run(self):
        from time import sleep
        self.running = True
        while self.running:
            self.run_once()
            sleep(self.dt)

    def start(self):
        from ubcs_auxiliary.threading import new_thread
        new_thread(self.run,)

    def stop(self):
        self.running = False
