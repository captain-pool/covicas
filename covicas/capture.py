import cv2
import os
from .face_extract import Extract
class Capture:
    def __init__(self,raspi = False,source = 0,target_dir = "."):
        self.__fg = Extract(source = source,raspi = raspi)
        self.__cap = 0
        self.__break = False
        if os.path.exists(os.path.abspath(target_dir)):
            self.__target_dir = target_dir
    def capture(self):
        self.__cap = 1
    def show(self):
        while True:
            if self.__break:
                break
            i = next(self.__fg)
            if self.__cap == 0:
                if len(i) == 3:
                    (x,y,w,h) = i[0]
                    cv2.rectangle(i[2],(x,y),(x+w,y+h),(0,255,0),2)
                    face = i[1]
                    i = i[2]
                cv2.imshow("capture",i)
                if cv2.waitKey(1)&0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    break
            else:
                self.save(face,"capture")
    def save(self,frame,filename):
        path = os.path.join(self.__target_dir,filename)
        count = 0
        while True:
            if os.path.exists(path+"_%d.jpg"%count):
                count+=1
            else:
                break
        cv2.imwrite(path+"_%d.jpg"%count,frame)
        print("\nSAVED as %s"%os.path.basename(path+"_%d.jpg"%count))
        self.__cap = 0
    def close(self):
        self.__break = True
        cv2.destroyAllWindows()
        self.__fg.close()
