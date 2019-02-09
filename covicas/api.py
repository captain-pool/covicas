from flask import Flask,jsonify
class Response:
    def __init__(self,settings = {},generator = None):
        self.gen = generator
        self.app = Flask(__name__)
        self.route_set = False
        self.settings = settings
    def __fetcher(self):
        return jsonify(next(self.gen))
    def run(self,target = "/",method = ["get"]):
        if not self.route_set:
            self.app.route(target,methods = method)(self.__fetcher)
            self.route_set = True
        self.app.run(host = self.settings.get("host","127.0.0.1"),port = self.settings.get("port",8000),debug = self.settings.get("debug1",False))
