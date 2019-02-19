from flask import Flask,jsonify
from flask_cors import CORS,cross_origin
class Response:
    def __init__(self,settings = {},generator = None):
        self.gen = generator
        self.app = Flask(__name__)
        CORS(self.app,support_credentials = True)
        self.route_set = False
        self.settings = settings
    @cross_origin(support_credentials = True)
    def __fetcher(self):
        return jsonify(next(self.gen))
    def run(self,target = "/",method = ["get"]):
        if not self.route_set:
            self.app.route(target,methods = method)(self.__fetcher)
            self.route_set = True
        self.app.run(host = self.settings.get("host","127.0.0.1"),port = self.settings.get("port",8000),debug = self.settings.get("debug1",False))
