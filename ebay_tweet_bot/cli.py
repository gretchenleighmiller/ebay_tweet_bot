from datetime import datetime
import logging
from os import environ, path
from sys import argv
from ebay_tweet_bot import Config
from ebay_tweet_bot import MongoConnection
from ebay_tweet_bot import EbayParser
from ebay_tweet_bot import Tweeter


class App:
    def __init__(self, mode):
        self.base_path = environ['EBAY_TWEET_BOT_BASE_PATH']
        self.mode = mode
        self.config_logger()
        self.run()

    def run(self):
        if self.mode == 'json':
            config_file = path.join(self.base_path,
                                    environ['EBAY_TWEET_BOT_CONFIG_FILE'])
            logging.info('Starting')
            logging.info('Loading config from JSON')
            config = Config()
            config.load_from_disk(config_file)
            if len(config.search_profile) == 0:
                logging.info('Search profile not present')
                logging.info('Exiting without finishing')
                return
            self.process_config(config)
            config.set_last_run(datetime.utcnow().isoformat())
            logging.info('Saving updated config')
            config.save_to_disk(config_file)
        if self.mode == 'mongodb':
            logging.info('Setting up MongoDB connection')
            mongo_host = environ['MONGO_HOST']
            mongo_port = int(environ['MONGO_PORT'])
            mongo_connection = MongoConnection(mongo_host, mongo_port)
            config_records = mongo_connection.get_config_records()
            for config_record in config_records:
                config = Config()
                config.load_from_mongodb(config_record)
                if len(config.search_profile) == 0:
                    logging.info('Search profile not present')
                    continue
                self.process_config(config)
                config.set_last_run(datetime.utcnow().isoformat())
                logging.info('Saving updated config')
                config.save_to_mongodb(mongo_connection)
        logging.info('All done!')

    def config_logger(self):
        log_file_path = path.join(self.base_path, 'ebay_twitterbot.log')
        logging.basicConfig(filename=log_file_path, level=logging.INFO,
                            format='%(asctime)s %(levelname)s:%(message)s')
        # make requests logging less noisy
        logging.getLogger("requests").setLevel(logging.WARNING)

    def process_config(self, config):
        logging.info('Constructing eBay API parser from config')
        parser = EbayParser(config)
        parser.make_payload()
        logging.info('Retrieving and parsing results')
        logging.info(parser.payload)
        parser.make_request()
        parser.parse_response()
        if len(parser.listings) != 0:
            logging.info('Found %d results', len(parser.listings))
            logging.info('Constructing Twitter API object')
            twitter_config = config.get_twitter_config()
            tweeter = Tweeter(*twitter_config)
            logging.info('Tweeting listings')
            for listing in parser.listings:
                logging.info('Tweeting listing with title %s', listing[0])
                tweeter.send_tweet(listing)
        else:
            logging.info('No results found')


def main():
    try:
        App(argv[1])
    except Exception:
        print('Error, exiting...')
