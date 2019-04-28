import io
import numpy as np
import picamera
import cv2


class Capture:
    def __init__(self):
        self.__opened = True
        self.cam = picamera.PiCamera()

    def isOpened(self):
        return self.__opened

    def read(self):
        data = io.BytesIO()
        self.cam.capture(data, format="jpeg")
        ret = len(data.getvalue())
        if ret > 0:
            ret = True
        else:
            return False, None
        try:
            data = np.fromstring(data.getvalue(), dtype=np.uint8)
            img = cv2.imdecode(data, 1)
        except BaseException:
            return False, None
        return ret, img

    def release(self):
        self.__opened = False
        self.cam.close()
