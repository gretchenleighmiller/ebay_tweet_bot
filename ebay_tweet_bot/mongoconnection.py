from pymongo import MongoClient
from bson.objectid import ObjectId


class MongoConnection():

    def __init__(self, host, port):
        self.client = MongoClient(host, port)
        self.db = self.client.ebay_tweet_bot
        self.bots = self.db.bots

    def get_bots(self):
        return self.bots

    def update_bot(self, bot, time):
        self.bots.update_one(
            {'_id': ObjectId(bot['_id'])},
            {
                "$set": {
                    "last_run": time
                }
            })
