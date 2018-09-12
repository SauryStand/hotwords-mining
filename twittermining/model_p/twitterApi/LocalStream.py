
import datetime
from Basic import MongoDb

class LocalStream(object):
    def __init__(self):
        self.db = MongoDb().get_db()
        self.tweets = []