from covicas.capture import Capture
from covicas.settings import settings
import os
import tty
import termios
import sys
import cv2
import threading
if __name__ == "__main__":
    try:
        os.mkdir("db")
    except:
        pass
    db_folder = os.path.abspath("db")
    print("username: ",end = "")
    name = input()
    if not os.path.exists(os.path.join(db_folder,name)):
        os.mkdir(os.path.join(db_folder,name))
    cap = Capture(target_dir = os.path.join(db_folder,name))
    t1 = threading.Thread(target = cap.show)
    t1.start()
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)
    x = 0
    print("PRESS <ESC> to exit.")
    while x != chr(27):
        x = sys.stdin.read(1)[0]
        sys.stdout.flush()
        if x == "c":
            cap.capture()
    cap.close()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    print()
        
