from .settings import settings
from .lazy_loader import LazyLoader
import json
from paho.mqtt.client import Client
from collections import deque

class Response:
    def __init__(self, generator=None, master=False, **kwargs):
        self.gen = generator
        self.settings = settings()
        self.app = None
        self.modules = LazyLoader()
        self.client_list = []
        if master:
            # Lazy Loading For Master Node
            self.modules.import_(
                "Database",
                parent=".db_plugin",
                return_=False)
            self.modules.import_("Flask", parent="flask", return_=False)
            self.modules.import_("jsonify", parent="flask", return_=False)
            self.modules.import_("CORS", parent="flask_cors", return_=False)
            self.modules.import_("datetime", parent="datetime", return_=False)
            globals().update(self.modules.import_dict)
            self.route_set = False
            self.app = Flask(__name__)
            CORS(self.app)
            self.database_ = Database()
        else:
            IP = kwargs.get("IP", "127.0.0.1")
            self.client_ = Client()
            try:
                self.client_.connect(
                    IP, self.settings.get(
                        "mqtt_port", 1883), self.settings.get(
                        "mqtt_timeout", 60))
            except ConnectionRefusedError:
                if self.settings.get("debug", False):
                    raise
                raise OSError("Start mosquitto service on system.")
        self.master = master
        self.message_queue = deque()

    def __publish(self):
        while True:
            v = next(self.gen)
            self.client_.publish("topic/camera", json.dumps(v))

    def __on_connect(self, client, userdata, flags, rc):
        client.subscribe("topic/camera")

    def __on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        data["timestamp"] = str(datetime.now())
        self.database_.store(data)
        try:
            self.message_queue.append(data)
            if self.settings.get("MAX_MESSAGE_QUEUE", 1000) == len(self.message_queue): 
              self.message_queue.popleft()
        except BaseException:
            if settings.get("debug"):
                raise

    def __fetcher(self):
        data = {"num_faces": 0, "timestamp": str(datetime.now())}
        try:
            data = self.message_queue.pop()
        except IndexError:
            pass
        except BaseException:
            if self.settings.get("debug", False):
                raise
        self.database_.store(data)
        return jsonify(data)

    def __subscribe(self):
        ip_list = self.settings.get("slaves", ["127.0.0.1"])
        for ip in ip_list:
            client = Client()
            client.connect(ip, 1883, self.settings.get("mqtt_timeout", 60))
            client.on_connect = self.__on_connect
            client.on_message = self.__on_message
            client.loop_start()
            self.client_list.append(client)

    def close(self):
        if not self.master:
            self.client_list.append(self.client_)
        try:
            while True:
                self.client_list.pop().disconnect()
        except IndexError:
            pass

    def run(self):
        if not self.master:
            self.__publish()
        else:
            if not self.route_set:
                self.app.route(rule="/", methods=["GET"])(self.__fetcher)
                self.__subscribe()
                self.route_set = True
            self.app.run(
                host=self.settings.get(
                    "host", "127.0.0.1"), port=self.settings.get(
                    "port", 8000), debug=self.settings.get(
                    "debug1", False))
