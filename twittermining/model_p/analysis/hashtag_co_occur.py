# -*- coding:utf-8 -*-

import pymongo
import time
import datetime
import collections

if __name__ == '__main__':

    starttime = datetime.datetime.now()

    lower_bound = str(int(time.mktime(datetime.datetime(2015, 11, 15).timetuple())) * 1000)
    upper_bound = str(int(time.mktime(datetime.datetime(2015, 11, 17).timetuple())) * 1000)
    client = pymongo.MongoClient()
    db = client.twitter
    cursor = db.stream.aggregate()