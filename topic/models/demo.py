import threading
import time
import multiprocessing

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
        self.lock = threading.Lock()
        self.parent_conn, self.child_conn = multiprocessing.Pipe()


def main():

    topic_trends = TopicTrendsManager()
    #while True :


if __name__ == '__name__':
    main()