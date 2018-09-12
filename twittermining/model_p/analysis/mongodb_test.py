import pymongo

class mongodbTest(object):
    def test(self):
        client = pymongo.MongoClient()
        db = client.twitter
        return db.stream.find().limit(10)