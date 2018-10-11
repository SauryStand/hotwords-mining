# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/1/25.
import time
import datetime
from Basic import TwitterBasic
import twitter


class TwitterStream(TwitterBasic):
    def __init__(self, conn=None):
        TwitterBasic.__init__(self)

        self.conn = conn
        self.tweets = []
        self.get_data = False

    def ready_receive(self):
        self.get_data = True

    def stream_data(self, track=None, follow=None, locations=None, save_to_db=False,
                    collection_name='stream'):
        """
            https://dev.twitter.com/streaming/reference/post/statuses/filter
            The default access level allows up to 400 track keywords, 5,000 follow userids and 25 0.1-360 degree location boxes.

        :param track: str    ;
        :param follow:list str ;
        :param locations: str ;
        :param save_to_db:
        :param collection_name:
        :return: None
        """

        def location_bounding_box(_locations):
            t = _locations.split(',')
            res = ''
            for i in xrange(0, len(t), 2):
                x, y = str(float(t[i]) + 1), str(float(t[i + 1]) + 1)
                res += t[i] + ',' + t[i + 1] + ',' + x + ',' + y + ','
            return res

        kwg = {'language': 'en'}

        if not track and not follow and not locations:
            kwg['track'] = 'twitter'

        if track:
            kwg['track'] = track

        if follow:
            kwg['follow'] = follow

        if locations:
            kwg['locations'] = location_bounding_box(locations)

        print kwg

        twitter_stream = twitter.TwitterStream(auth=self.twitter_api.auth)
        stream = twitter_stream.statuses.filter(**kwg)

        for i, tweet in enumerate(stream):
            if not i % 200 and 'text' in tweet: print i, datetime.datetime.now(), ' ', tweet["text"]
            tweet = dict(tweet)
            if 'id' in tweet:
                self.tweets.append(tweet)

                if self.get_data:
                    self.get_data = False
                    self.conn.send(self.tweets)
                    self.tweets = []

                if save_to_db:
                    self.save_tweets_to_mongodb(tweet, colname=collection_name)


