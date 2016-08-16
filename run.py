# -*- coding: utf-8 -*-
import logging, sys, os
from datetime import datetime
from ebay_tweet_bot import Config, EbayParser, Tweeter

def main():
	# get full file paths in case script is called from another dir
	dir_path = os.path.dirname(sys.argv[0])
	log_file_path = os.path.join(dir_path, 'ebay_twitterbot.log')
	config_file_path = os.path.join(dir_path, 'config.json')
	logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
	# make requests logging less noisy
	logging.getLogger("requests").setLevel(logging.WARNING)
	logging.info('Starting')
	logging.info('Loading config from config.json')
	config = Config(config_file_path)
	if len(config.search_profile)==0:
		logging.info('Search profile not present')
		logging.info('Exiting without finishing')
		return
	logging.info('Constructing eBay API parser from config')
	parser = EbayParser(config)
	parser.make_payload()
	logging.info('Retrieving and parsing results')
	parser.make_request()
	parser.parse_response()
	if len(parser.listings)!=0:
		logging.info('Found %d results', len(parser.listings))
		logging.info('Constructing Twitter API object')
		tweeter = Tweeter(	config.twitter_consumer_key,
							config.twitter_consumer_secret,
							config.twitter_access_token_key,
							config.twitter_access_token_secret,
							config.bitly_access_token)
		logging.info('Tweeting listings')
		for listing in parser.listings:
			logging.info('Tweeting listing with title %s', listing[0])
			tweeter.send_tweet(listing)
	else:
		logging.info('No results found')
	logging.info('Updating last run time')
	config.set_last_run(datetime.utcnow().isoformat())
	logging.info('Saving updated config to config.json')
	config.save()
	logging.info('All done!')

if __name__ == '__main__':
	main()
