import time
import io
import threading
import picamera


class Camera(object):
    """Camera class"""

    thread = None  #thread reading frames
    img = None  #img saved by background thread
    last_access = 0  # time of last img sent
    activeClient = False #used for limiting number of clients to only one
    shouldStop = False #

    def __init__(self, car):
        self.car = car

    def get_img(self):
        """dsa"""
        self.last_access = time.time()
        #is the thread running?
        if self.thread is None:
            # start background thread
            self.thread = threading.Thread(target=self.back_thread)
            self.thread.start()


            # wait until frames are available
            while self.img is None:
                time.sleep(0)
        #print("returning frame")

        return self.img

    def back_thread(self):
        """"""
        print("Camera thead started")
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)

            time.sleep(2) #camera needs some time to get ready

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # store the frame
                stream.seek(0)
                self.img = stream.read()
                time.sleep(0)

                # reset for next frame
                stream.seek(0)
                stream.truncate()
                #calculate the time between last and actual request for img
                diff = time.time() - self.last_access
                #if the time is higher than 0.5s stop the car
                if diff < 0.5:
                    self.shouldStop = False
                    #print("Going again")
                else:
                    print("Stopping")
                    self.shouldStop = True
                    self.car.stop()
                    #if the diff is more than 4 seconds the client has probably disconnected so stop the thread
                    if diff > 4:
                        self.activeClient = False
                        print("Stopping Camer thread")
                        break

        self.thread = None
