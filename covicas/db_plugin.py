from tinydb import TinyDB, Query
import os
from .settings import settings
from .signals import Handler
import lockfile
import time
class Database:
    def __init__(self):
        self.settings = settings()
        self.db_name = self.settings.get("db_name", "database.json")
        self.db_ = TinyDB(self.db_name)
        self.query_ = Query()
        self._keyboard_interrupt = False
        handler = Handler()
        handler.register(self._handler)
        self._db_queue = []
    def _handler(self):
        self._keyboard_interrupt = True

    def _read(self):
        try:
            assert os.path.exists(self.db_name)
            obj_ = self.db_.all()
        except BaseException:
            obj_ = []
        return obj_

    def store(self, data):
        self._db_queue.append(data)
        if int(data["num_faces"]) != 0:
            self.db_.insert(data)
    def display(self, follow=False):
        assert os.path.exists(self.db_name)
        prev_len = 0
        curr_len = 1
        while True:
            object_ = self._read()
            curr_len = len(object_)
            if self._keyboard_interrupt:
                break
            if curr_len == prev_len:
                continue
            for i in object_:
                for j in i["faces"]:
                    print(
                        "[%s]: %s Camera: #%d" %
                        (i["timestamp"], j["label"], j["camera"]))
            if not follow:
                break
            prev_len = curr_len
        print("\n" + "-" * 30 + "\n[Exitting] . . . ")
