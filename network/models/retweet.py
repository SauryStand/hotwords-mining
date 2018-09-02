

from twittermining.mongodb_model import MongoDb,TimeCost

def get_retweet_data_by_time(time):
    db = MongoDb.getDB()
    field = {
        'id': 1,
        'text': 1,
        'user_id': 1,
        'retweet_id': 1,
        'retweet_count': 1,
        'user_mentions': 1,
    }
    cursor = db.stream.aggregate([
        {'$match': {'hashtags': 'Christmas'}},
        {'$sort': {'retweet_count': -1}},
        {'$limit': 10},
        # {'$project': field}
    ], )
    tweets = [tweet for tweet in cursor]
    cursor = db.stream.aggregate([
        {'$match': {'retweet_id': {'$in': [tweet['id'] for tweet in tweets]}}},
        # {'$project': field}
    ], )
    tweets += [tweet for tweet in cursor]
    return tweets


#todo