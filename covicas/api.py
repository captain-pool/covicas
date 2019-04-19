from .settings import settings
import json
from paho.mqtt.client import Client
class Response:
  def __init__(self,generator=None, master=False, **kwargs):
    self.gen = generator
    self.settings = settings()
    self.app = None
    self.client_list = []
    if master:
      # Lazy Loading For Master Node
      from db_plugin import Database
      from flask import Flask, jsonify
      from flask_cors import CORS
      from datetime import datetime
      
      self.route_set = False
      self.app = Flask(__name__)
      CORS(self.app)
      self.database_ = Database()
    else:
      IP = kwargs.get("IP", "localhost")
      self.client_ = Client()
      try:
        self.client_.connect(IP, self.settings.get("mqtt_port",1883), self.settings.get("mqtt_timeout", 60))
      except ConnectionRefusedError:
        if self.settings.get("debug", False):
          raise
      print("Start mosquitto service on system.")
    self.master = master
    self.message_queue = []
  def __publish(self):
    while True:
      v = next(self.gen)
      self.client.publish("topic/camera",json.dumps(v))
  def __on_connect(self, client, userdata, flags, rc):
    client.subscribe("topic/camera")
  def __on_message(self, client, userdata, msg):
    data = msg.payload.decode()
    try:
      self.message_queue.append(json.loads(data))
    except:
      if settings.get("debug"):
        raise
  def __fetcher(self):
    data = {"num_faces": 0}
    try:
      data = self.message_queue.pop()
    except IndexError:
      pass
    except:
      if self.settings.get("debug", False):
        raise
    data["timestamp"] = str(datetime.now())
    return jsonify(data)

  def __subscribe(self):
    ip_list = self.setttings.get("slaves")
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
        self.app.route(target="/", methods=["GET"])(self.__fetcher)
        self.route_set = True
      self.app.run(host = self.settings.get("host","127.0.0.1"),port = self.settings.get("port",8000),debug = self.settings.get("debug1",False))
