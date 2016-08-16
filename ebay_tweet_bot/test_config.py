# -*- coding: utf-8 -*-

import sys, os, unittest
from datetime import datetime, timedelta
from ebay_tweet_bot import Config

class ConfigTester(unittest.TestCase):
	def setUp(self):
		self.dir_path = os.path.dirname(sys.argv[0])
		self.dir_path = os.path.join(self.dir_path, 'test_data')
		self.config_file_path = os.path.join(self.dir_path, 'test_config.json')
		self.config = Config(self.config_file_path)

	def testEbayApiAppId(self):
		self.assertIsNotNone(self.config.ebay_api_app_id)

	def testTwitterApiConfig(self):
		self.assertIsNotNone(self.config.twitter_consumer_key)
		self.assertIsNotNone(self.config.twitter_consumer_secret)
		self.assertIsNotNone(self.config.twitter_access_token_key)
		self.assertIsNotNone(self.config.twitter_access_token_secret)

	def testBitlyAccessToken(self):
		self.assertIsNotNone(self.config.bitly_access_token)

	def testSaveLastRunTime(self):
		self.config.set_last_run((datetime.utcnow()-timedelta(hours=12)).isoformat())
		old_last_run = self.config.last_run
		self.config.save()
		self.config.load()
		self.assertEqual(old_last_run, self.config.last_run)




