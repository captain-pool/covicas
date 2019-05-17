import json
import os
from .settings import settings, singleton
from .signals import Handler
import lockfile
class Database:
    def __init__(self):
        self.settings = settings()
        self.db_name = self.settings.get("db_name", "database.json")
        self._keyboard_interrupt = False
        handler = Handler()
        handler.register(self._handler)
        self._db_queue = []
    def _handler(self):
        self._keyboard_interrupt = True

    def _read(self):
        try:
            assert os.path.exists(self.db_name)
            with lockfile.FileLock(self.db_name), open(self.db_name, "r") as f:
                obj_ = json.load(f)
        except BaseException:
            obj_ = []
        return obj_

    def store(self, data):
        object_ = self._read()
        self._db_queue.append(data)
        with lockfile.FileLock(self.db_name), open(self.db_name, "w") as f:
            if int(data["num_faces"]) != 0:
                object_.append(self._db_queue.pop())
                json.dump(object_, f)

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
