from covicas.lazy_loader import LazyLoader
from covicas.signals import Handler
from absl import app, flags
handler = Handler()
lazy_ = LazyLoader()
FLAGS = flags.FLAGS
flags.DEFINE_boolean(
    "master",
    False,
    " Sets the Network API Mode to Master Mode (True) / Slave Mode (False)")
flags.DEFINE_string("cam", "0", "<WebCamera Number>/ raspi")
flags.DEFINE_string("settings", "settings.json", "Settings File to use")
response = None
@handler.register
def handler():
    print(" User Interrupt. Exiting ... ")
    try:
        s = settings()
        s.close()
        del(s)
    except:
        pass
    if not response is None and hasattr(response, 'close'):
        response.close()
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
        except BaseException:
            raise ValueError
    print("Booting Up ...")
    lazy_.import_("cv2", return_=False)
    lazy_.import_("LBPHClassifier", alias="lc", parent="covicas.model", return_=False)
    lazy_.import_("Extract", parent="covicas.face_extract", return_=False)
    lazy_.import_("Response", parent="covicas.api", return_=False)
    lazy_.import_("settings", parent="covicas.settings", return_=False)
    globals().update(lazy_.import_dict)
    s = settings(FLAGS.settings)
    # s.set("debug",True)
    gen = None
    if not FLAGS.master:
        print("Selecting Slave Mode ... ", end="")
        e = Extract(source=cam_num, channel="GRAY", raspi=raspi)
        m = lc(type=lc.EXEC, frame_gen=e, trained_model="saved_model.yml")
        gen = m.read()
    else:
        print("Selecting Master Mode ... ", end="")
    response = Response(generator=gen, settings=s, master=FLAGS.master)
    print("[READY]")
    response.run()
    if s.get("debug", False):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app.run(main)
