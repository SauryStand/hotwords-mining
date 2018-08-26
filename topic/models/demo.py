import threading
import time

class Singleton(type):
    _instances = []

    def __call__(cls_self, *args, **kwargs):
        if cls_self not in cls_self._instances:
            cls_self._instances[cls_self] = super(Singleton,cls_self).__call__(*args, **kwargs)
        return cls_self._instances[cls_self]


class TopicTrendsManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.topics = []

def main():

    #while True :


if __name__ == '__name__':
    main()