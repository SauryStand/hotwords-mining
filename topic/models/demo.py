import threading
import time

class Singleton(type):
    _instances = []

    def __call__(cls_self, *args, **kwargs):
        if cls_self not in cls_self._instances:
            cls_self._instances[cls_self] = super(Singleton,cls_self).__call__(*args, **kwargs)
        return cls_self._instances[cls_self]


def main():

    while True :


if __name__ == '__name__':
    main()