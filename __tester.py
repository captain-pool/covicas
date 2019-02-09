from covicas.model import LBPHClassifier as lc
from covicas.face_extract import Extract
from covicas.api import Response
import cv2
from covicas.settings import settings
s = settings("abcd.json")
#s.set("debug",True)
print("Booting Up... ",end = "")
e = Extract(channel = "GRAY")
m = lc(type = lc.EXEC,frame_gen = e,trained_model = "saved_model.yml")
gen = m.read()
print("[READY]")
r = Response(generator = gen,settings = s)
r.run()
if s.get("debug",False):
    cv2.destroyAllWindows()
