# -*- coding: utf-8 -*-

import sys, os, unittest
from datetime import datetime
from ebay_tweet_bot import Config, Tweeter

class TweeterTest(unittest.TestCase):
	def setUp(self):
		self.dir_path = os.path.dirname(sys.argv[0])
		self.dir_path = os.path.join(self.dir_path, 'test_data')
		self.config_file_path = os.path.join(self.dir_path, 'test_config.json')
		config = Config(self.config_file_path)
		self.tweeter = Tweeter(	config.twitter_consumer_key,
								config.twitter_consumer_secret,
								config.twitter_access_token_key,
								config.twitter_access_token_secret,
								config.bitly_access_token)

	def testTweetWithImage(self):
		listing_with_image = ('Test Tweet With Image ' + datetime.utcnow().isoformat(), 99.99, os.path.join(self.dir_path, 'Testcard_F.jpg'), 'http://www.ebay.com')
		tweet_status = self.tweeter.send_tweet(listing_with_image)
		self.assertIsNotNone(tweet_status.id)
		self.assertIn(listing_with_image[0], tweet_status.text)
		self.assertIsNotNone(tweet_status.media)
		self.assertEqual(len(tweet_status.media), 1)
		self.assertEqual(tweet_status.media[0].type, 'photo')

	def testTweetWithoutImage(self):
		listing_without_image = ('Test Tweet Without Image ' + datetime.utcnow().isoformat(), 88.88, None, 'http://www.ebay.com')
		tweet_status = self.tweeter.send_tweet(listing_without_image)
		self.assertIsNotNone(tweet_status.id)
		self.assertIn(listing_without_image[0], tweet_status.text)
		self.assertIsNone(tweet_status.media)
