# -*- coding: utf-8 -*-
import logging
import sys
import os
from datetime import datetime
from ebay_tweet_bot import EbayParser, Tweeter, MongoConnection


def main():
    # get full file paths in case script is called from another dir
    dir_path = os.path.dirname(sys.argv[0])
    log_file_path = os.path.join(dir_path, 'ebay_twitterbot.log')
    logging.basicConfig(filename=log_file_path, level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(message)s')
    # make requests logging less noisy
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.info('Starting')
    logging.info('Setting up MongoDB connection')
    mongo_host = os.environ['MONGO_HOST']
    mongo_port = int(os.environ['MONGO_PORT'])
    mongo_connection = MongoConnection(mongo_host, mongo_port)
    logging.info('Getting bots from MongoDB')
    bots = mongo_connection.get_bots()

    for bot in bots.find():
        logging.info('Constructing eBay API parser from bot')
        parser = EbayParser(bot)
        parser.make_payload()
        logging.info('Retrieving and parsing results')
        logging.info(parser.payload)
        parser.make_request()
        parser.parse_response()
        if len(parser.listings) != 0:
            logging.info('Found %d results', len(parser.listings))
            logging.info('Constructing Twitter API object')
            tweeter = Tweeter(
                bot['twitter_api_config']['consumer_key'],
                bot['twitter_api_config']['consumer_secret'],
                bot['twitter_api_config']['access_token_key'],
                bot['twitter_api_config']['access_token_secret'],
                bot['bitly_access_token']
            )
            logging.info('Tweeting listings')
            for listing in parser.listings:
                logging.info('Tweeting listing with title %s', listing[0])
                tweeter.send_tweet(listing)
        else:
            logging.info('No results found')
        logging.info('Updating last run time')
        logging.info('Saving updated config to config.json')
        mongo_connection.update_bot(bot, datetime.utcnow().isoformat())
        logging.info('All done!')


if __name__ == '__main__':
    main()
