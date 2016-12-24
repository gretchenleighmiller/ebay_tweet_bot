import json
import logging


class Config():
    def __init__(self):
        self.config_dict = {}
        self.ebay_api_app_id = None
        self.search_profile = {}
        self.twitter_consumer_key = None
        self.twitter_consumer_secret = None
        self.twitter_access_token_key = None
        self.twitter_access_token_secret = None
        self.bitly_access_token = None
        self.last_run = None

    def load_from_disk(self, config_file):
        try:
            with open(config_file, mode='r', encoding='utf-8') as f:
                self.config_dict = json.load(f)
        except Exception as e:
            logging.error(e)
            return
        self.load()

    def load_from_mongodb(self, config_record):
        self.config_dict = config_record
        self.load()

    def load(self):
        self.ebay_api_app_id = self.config_dict['ebay_api_app_id']
        self.search_profile = self.config_dict['search_profile']
        self.twitter_consumer_key = self.config_dict['twitter_api_config']['consumer_key']
        self.twitter_consumer_secret = self.config_dict['twitter_api_config']['consumer_secret']
        self.twitter_access_token_key = self.config_dict['twitter_api_config']['access_token_key']
        self.twitter_access_token_secret = self.config_dict['twitter_api_config']['access_token_secret']
        self.bitly_access_token = self.config_dict['bitly_access_token']
        self.last_run = self.config_dict['last_run']

    def set_last_run(self, time):
        self.last_run = time

    def save_to_disk(self, config_file):
        self.config_dict = {
            'ebay_api_app_id': self.ebay_api_app_id,
            'search_profile': self.search_profile,
            'twitter_api_config': {
                'consumer_key': self.twitter_consumer_key,
                'consumer_secret': self.twitter_consumer_secret,
                'access_token_key': self.twitter_access_token_key,
                'access_token_secret': self.twitter_access_token_secret
            },
            'last_run': self.last_run,
            'bitly_access_token': self.bitly_access_token
        }
        try:
            with open(config_file, mode='w', encoding='utf-8') as f:
                f.write(json.dumps(self.config_dict, indent=4, sort_keys=True))
        except Exception as e:
            logging.error(e)
            logging.warning('Could not save JSON file')
            return

    def save_to_mongodb(self, mongo_connection):
        mongo_connection.update_config_record(
            self.config_dict['_id'],
            {'last_run': self.last_run}
        )

    def get_twitter_config(self):
        twitter_config = (
            self.twitter_consumer_key,
            self.twitter_consumer_secret,
            self.twitter_access_token_key,
            self.twitter_access_token_secret,
            self.bitly_access_token
        )
        return twitter_config
