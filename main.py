from covicas.model import LBPHClassifier as lc
from covicas.face_extract import Extract
from covicas.api import Response
from covicas.signals import Handler
import cv2
from absl import app,flags
from covicas.settings import settings
handler = Handler()
FLAGS = flags.FLAGS
flags.DEFINE_boolean("master", False, " Sets the Network API Mode to Master Mode (True) / Slave Mode (False)")
flags.DEFINE_string("cam","0","<WebCamera Number>/ raspi")
flags.DEFINE_string("settings","settings.json","Settings File to use")
response = None
@handler.register
def handler():
    print(" User Interrupt. Exiting ... ")
    s = settings()
    s.close()
    if not response is None and hasattr(response, 'close'):
      response.close()
    del(s)
    exit(0)
def main(argv):
    del argv
    global response
    raspi = False
    cam_num = 0
    if FLAGS.cam == "raspi":
        raspi = True
    else:
        try:
            cam_num = int(FLAGS.cam)
        except:
            raise ValueError    
    print("Booting Up ...")
    s = settings(FLAGS.settings)
    #s.set("debug",True)
    gen = None
    if not FLAGS.master:
      print("Selecting Slave Mode ... ", end="")
      e = Extract(source = cam_num,channel = "GRAY",raspi = raspi)
      m = lc(type = lc.EXEC,frame_gen = e,trained_model = "saved_model.yml")
      gen = m.read()
    else:
      print("Selecting Master Mode ... ", end="")
    response = Response(generator = gen,settings = s, master=FLAGS.master)
    print("[READY]")
    response.run()
    if s.get("debug",False):
        cv2.destroyAllWindows()
if __name__ == "__main__":
    app.run(main)
