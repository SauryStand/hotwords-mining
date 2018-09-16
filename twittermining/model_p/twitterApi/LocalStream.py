
import datetime
from Basic import MongoDb

class LocalStream(object):
    def __init__(self):
        self.db = MongoDb().get_db()
        self.tweets = []

    def stream_date(self,condition,start_time,end_time,collection_name='stream'):
        start = end = None
        try:
            start = datetime.datetime.strptime(start_time, '%Y-%m-%d')
            end = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        except Exception as e:
            pass

        match = {
            '$match': {
                'date': {
                }
            }}
        if start:
            match['$match']['date']['$gt'] = start
        if end:
            match['$match']['date']['$lt'] = end

        pipeline = []
        if start and end:
            pipeline.append(match)
            pipeline.append({'$sort': {'date': 1}})

        cursor = self.db[collection_name].aggregate(pipeline)

        if condition.acquire():
            print
            'loading local data'
            for doc_chunk in chunkize_serial(cursor, 3000, as_numpy=False):
                print
                doc_chunk[0]
                self.tweets = doc_chunk
                condition.notify()
                condition.wait()