import signal
import functools
from .settings import *
@singleton
class Handler:
    def __init__(self):
        self._functions = []
        signal.signal(signal.SIGINT, self.__handler)

    def __handler(self, signum, handler):
        for func in self._functions[::-1]:
            if callable(func):
                func()
            else:
                print(
                    "WARNING: Object \"%s\" is not Callable. Ignoring Exection..." %
                    func)

    def register(self, func):
        self._functions.append(func)
        return func
