import json
import os
def singleton(cls):
    instances = {}
    def getinstance(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return getinstance
@singleton
class settings:
    def __init__(self,_json):
        self._json = {}
        _json = os.path.abspath(_json)
        if os.path.exists(_json) and not os.path.isdir(_json) and os.path.getsize(_json)>0:
            with open(_json,"r") as f:
                self._json = json.load(f)
        self._fp = open(_json,"a")
    #    settings.__count += 1
    def __del__(self):
        self._fp.truncate(0)
        json.dump(self._json,self._fp)
        self._fp.close()
    def get(self,key,default = None):
        return self._json.get(key,default)
    def set(self,key,val):
        self._json[key] = val
        
