import threading
import time


class MyThread(threading.Thread):
    def run(self):                                         # Default called function with mythread.start()
        print("{} started!".format(self.getName()))        # "Thread-x started!"
        time.sleep(1)                                      # Pretend to work for a second
        print("{} finished!".format(self.getName()))       # "Thread-x finished!"

def main():
    for x in range(4):                                     # Four times...
        mythread = MyThread(name = "Thread-{}".format(x))  # ...Instantiate a thread and pass a unique ID to it
        mythread.start()                                   # ...Start the thread, run method will be invoked
        # time.sleep(.5)                                     # ...Wait 0.9 seconds before starting another

if __name__ == '__main__':
    main()