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
    except BaseException:
        pass
    db_folder = os.path.abspath("db")
    print("username: ", end="")
    name = input()
    if not os.path.exists(os.path.join(db_folder, name)):
        os.mkdir(os.path.join(db_folder, name))
    cap = Capture(target_dir=os.path.join(db_folder, name))
    cap.show(auto_cap=True)
    cap.close()
