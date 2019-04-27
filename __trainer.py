from covicas.model import LBPHClassifier as lc
from covicas.settings import settings
s = settings("settings.json")
s.set("CAM_NUM",1)
m = lc(type = lc.TRAIN,datadir = "./db")
m.read()
m.train()
