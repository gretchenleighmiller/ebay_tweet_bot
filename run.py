# -*- coding: utf-8 -*-
from ebay_tweet_bot import Config, EbayParser, Tweeter

def main():
	config = Config('config.json')
	parser = EbayParser(config)
	parser.make_payload()
	parser.make_request()
	parser.parse_response()
	tweeter = Tweeter(	config.twitter_consumer_key,
						config.twitter_consumer_secret,
						config.twitter_access_token_key,
						config.twitter_access_token_secret)
	for listing in parser.listings:
		tweeter.send_tweet(listing)

if __name__ == '__main__':
	main()
