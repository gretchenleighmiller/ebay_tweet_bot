from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
import sys
import traceback


class MongoConnection():

    def __init__(self, host, port):
        self.client = MongoClient(host, port)
        self.db = self.client.ebay_tweet_bot

    def get_config_records(self):
        return self.db.config_records.find()

    def update_config_record(self, config_record_id, set_dict):
        config_record_id = {'_id': ObjectId(config_record_id)}
        update_dict = {}
        update_dict['$set'] = {}
        for key, value in set_dict.items():
            update_dict['$set'][key] = value
        try:
            self.db.config_records.update_one(config_record_id, update_dict)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(
                exc_type,
                exc_value,
                exc_traceback
            )
            logging.warning(''.join('!!' + line for line in lines))
