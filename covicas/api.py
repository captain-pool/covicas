from flask import Flask,jsonify
from datetime import datetime
from flask_cors import CORS,cross_origin
from .db_plugin import Database
class Response:
    def __init__(self,settings = {},generator = None):
        self.gen = generator
        self.database_ = Database()
        self.app = Flask(__name__)
        CORS(self.app,support_credentials = True)
        self.route_set = False
        self.settings = settings
    @cross_origin(support_credentials = True)
    def __fetcher(self):
        v = next(self.gen)
        v["timestamp"] = str(datetime.now())
        self.database_.store(v)
        return jsonify(v)
    def run(self,target = "/",method = ["get"]):
        if not self.route_set:
            self.app.route(target,methods = method)(self.__fetcher)
            self.route_set = True
        self.app.run(host = self.settings.get("host","127.0.0.1"),port = self.settings.get("port",8000),debug = self.settings.get("debug1",False))
