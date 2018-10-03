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
    cursor = db.stream.aggregate([
        {
            '$match': {
                'timestamp_ms': {
                    '$gt': lower_bound,
                    '$lt': upper_bound,
                },
                'entities.hashtags.0': {
                    '$exists': 'true'
                }
            }
        },
        {
            '$project': {
                'entities.hashtags': 1
            }
        }
    ])
    cnt = 0
    hashtag_dic = collections.defaultdict(lambda: collections.defaultdict(int), {})
    for tweet in cursor:
        cnt += 1
        hashtags = tweet['entities']['hashtags']
        hashtags_len = len(hashtags)