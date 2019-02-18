import dlib
import cv2
try:
    from . import picap
except:
    pass
import sys
from .exceptions import *
import os
import numpy as np
from imutils import face_utils
class Extract:
    def __init__(self,source = 0,raspi = False,frame_drop = 0,faceWidth = 256,faceHeight = None,flipped = True,landmarkFile = "shape_predictor_68_face_landmarks.dat",channel = "BGR"):
        '''
            @param source: 0 #Video Source (`0` captures the Main Webcam if available)
            @param frame_drop: 0 #Number of Consecutive Frames to avoid Processing
            @param faceWidth: 256 #Desired Image Width of the Detected Face
            @param faceHeight: None #Desired Image Height of the detected Face (`None` gives a square image of dimensions FaceWidth x FaceWidth)
            @param flipped: True #Return Vertically Flipped Frames
            @param landmarkFile: "shape_predictor_68_face_landmarks.dat" #Location of Pretrained Weights of the Face Detector
        '''
        try:
            assert type(source) == int or type(source) == str
            if type(source) == str:
                assert os.path.exists(source)
            if not raspi:
                self.cap = cv2.VideoCapture(source)
                print("Selecting webcam ...")
            else:
                self.cap = picap.Capture()
                print("Selecting PiCam ...")
        except AssertionError:
            print("Invalid or Non Existent Source")
            raise
        self.flipped = flipped
        self.detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(landmarkFile)
        self.fa = face_utils.FaceAligner(predictor,desiredFaceWidth =faceWidth,desiredFaceHeight = faceHeight)
        self.frame_drop = frame_drop
        if channel == "RGB":
            self.out_channel = 0
        elif channel == "BGR":
            self.out_channel = 1
        elif channel == "GRAY":
            self.out_channel = 2
        else:
            raise ValueError("channel can be either of: \"RGB\"/\"BGR\",\"GRAY\"")
        # Generator Vairables
        self.frame_counter = 0
    def __next__(self):
        if not self.cap.isOpened():
            raise CameraNotOpenError
        while self.cap.isOpened():
            ret,img = self.cap.read()
            if ret:
                if self.flipped:
                    img = cv2.flip(img,1)
                if not self.frame_counter:
                    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    rects = self.detector(gray,1)
                if self.frame_drop:
                    self.frame_counter = (self.frame_counter+1)%self.frame_drop
                for rect in rects:
                    aligned = self.fa.align(img,gray,rect)
                    if self.out_channel == 0:
                        aligned = cv2.cvtColor(aligned,cv2.COLOR_BGR2RGB)
                    if self.out_channel == 2:
                        aligned = cv2.cvtColor(aligned,cv2.COLOR_BGR2GRAY)
                    bb = face_utils.rect_to_bb(rect)
                    return bb,aligned,img,len(rects)
                return img,0
    def close(self):
        self.cap.release()
