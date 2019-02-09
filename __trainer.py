from covicas.model import LBPHClassifier as lc
from covicas.settings import settings
s = settings("abcd.json")
m = lc(type = lc.TRAIN,datadir = "./db")
m.read()
m.train()
