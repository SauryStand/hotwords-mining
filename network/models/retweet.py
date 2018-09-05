

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
def get_retweet_network_nodes_and_links(date='2015-11-22'):
    tweets = get_retweet_data_by_time(date)
    tweets_id = set([tweet['id'] for tweet in tweets] + [tweet.get('retweet_id', 0) for tweet in tweets])
    id_num = {_id: i for i, _id in enumerate(tweets_id)}
    user_tweet_id_num = {tweet['user_id']: id_num[tweet['id']] for tweet in tweets}
    nodes = [{"id": node} for node in tweets_id]
    links = [{
        'source': id_num[tweet['id']],
        'target':
            user_tweet_id_num[tweet['user_mentions'][0]['id_str']]
            if 'user_mentions' in tweet and tweet['user_mentions'][0]['id_str'] in user_tweet_id_num else
            id_num[tweet.get('retweet_id', 0)]
    }
        for tweet in tweets]

    return {'nodes': nodes, 'links': links}


if __name__ == '__main__':
    get_retweet_network_nodes_and_links("")