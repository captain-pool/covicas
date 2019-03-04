from .settings import settings
import cv2
import glob
from .exceptions import *
import numpy as np
import tqdm
import os
class LBPHClassifier:
    #constants
    TRAIN = 0
    EXEC = 1
    def __init__(self,frame_gen=None,type = TRAIN,datadir = None,trained_model = None):
        
        if type == LBPHClassifier.TRAIN and datadir is None:
            raise TrainDataSourceNotProvidedError
        elif type == LBPHClassifier.EXEC and frame_gen is None:
            raise InvalidGeneratorError
        elif type == LBPHClassifier.TRAIN:
            self._datadir = datadir
            
        self.model = cv2.face.LBPHFaceRecognizer_create()
        if type == LBPHClassifier.EXEC:
            self._fgen = frame_gen
            if "saved_model.yml" in os.listdir("."):
                trained_model = "saved_model.yml"
            elif trained_model is None:
                raise TrainedModelNotProvidedError
            self.model.read(trained_model)
        self._type = type
        self.__database = None
        self.__lmap = None
    def read(self):
        if self._type == LBPHClassifier.TRAIN:
            self._read_files()
        if self._type == LBPHClassifier.EXEC:
            return self._read_live_frames()
    def _read_files(self):
        print("Building Database ... ",end = "")
        ext = "jpg png".split()
        path = os.path.abspath(self._datadir)
        names = [os.path.join(path,i) for i in os.listdir(path) if not os.path.isdir(i)]
        database = {}
        for i in names:
            files = []
            for j in ext:
                l = glob.glob(os.path.join(i,"*.{}".format(j)))
                files.extend(l)
            database[os.path.basename(i)] = files
        self.__database = database

        lmap = dict(enumerate(database.keys()))
        self.__lmap = lmap
        self.__invlmap = dict(zip(lmap.values(),lmap.keys()))
        sett = settings()
        sett.set("labelmap",lmap)
        print("[DONE]")
    def train(self):
        images = []
        labels = []
        print("Loading Dataset . . .",end = "")
        for k,v in tqdm.tqdm(self.__database.items(),ascii = True):
            for i in v:
                images.append(cv2.imread(i,cv2.IMREAD_GRAYSCALE))
                labels.append(self.__invlmap.get(k,-1))
        labels = np.array(labels)
        print("[DONE]")
        print("Training . . .",end = "")
        self.model.train(images,labels)
        print("[DONE]")
        sett = settings()
        self.model.write(sett.get("weightsFile","saved_model.yml"))
    def predict(self,frame,bb):
        sett = settings()
        if not self.__lmap:
            self.__lmap = sett.get("labelmap")
            if not self.__lmap:
                raise DataBaseNotBuiltError
        label,conf = self.model.predict(frame)
        return_dict = {}
        return_dict["label"] = self.__lmap.get(str(label),None)
        return_dict["confidence"] = conf
        return_dict["x"] = bb[0]
        return_dict["y"] = bb[1]
        return_dict["w"] = bb[2]
        return_dict["h"] = bb[3]
        return return_dict
    def __fetch_generator(self):
        try:
            return next(self._fgen)
        except:
            raise
    def _read_live_frames(self):
        s = settings() 
        while True:
            i = self.__fetch_generator()
            num = i[-1]
            print(len(i))
            json_list = {"num_faces":0}
            if i[-1] > 0:
                json_list["num_faces"] = num
                json_list["faces"] = []
                for idx in range(num):
                    label = self.predict(i[1],i[0])
                    if s.get("debug",False):
                        #DEBUG
                        print(s.__dict__)
                        (x,y,w,h) = i[0]
                        cv2.rectangle(i[2],(x,y),(x+w,y+h),(0,255,0),2)
                        cv2.putText(i[2],label["label"],(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),lineType=cv2.LINE_AA)
                        cv2.imshow("feed",i[2])
                        cv2.waitKey(1)
                        #DEBUG
                    json_list["faces"].append(label)
                    i = self.__fetch_generator()

            json_list["cam_num"] = s.get("CAM_NUM",0)
            yield json_list
