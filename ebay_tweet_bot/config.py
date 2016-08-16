# -*- coding: utf-8 -*-
import json, logging

class Config():
	def __init__(self, json_file):
		self.json_file = json_file
		self.ebay_api_app_id = None
		self.search_profile = {}
		self.twitter_consumer_key = None
		self.twitter_consumer_secret = None
		self.twitter_access_token_key = None
		self.twitter_access_token_secret = None
		self.bitly_access_token = None
		self.last_run = None
		self.load()

	def load(self):
		config_dict = {}

		try:
			with open(self.json_file, mode='r', encoding='utf-8') as f:
				config_dict = json.load(f)
		except Exception as e:
			logging.error(e)
			return
		self.ebay_api_app_id = config_dict['ebay_api_app_id']
		self.search_profile = config_dict['search_profile']
		self.twitter_consumer_key = config_dict['twitter_api_config']['consumer_key']
		self.twitter_consumer_secret = config_dict['twitter_api_config']['consumer_secret']
		self.twitter_access_token_key = config_dict['twitter_api_config']['access_token_key']
		self.twitter_access_token_secret = config_dict['twitter_api_config']['access_token_secret']
		self.bitly_access_token = config_dict['bitly_access_token']
		self.last_run = config_dict['last_run']

	def set_last_run(self, time):
		self.last_run = time

	def save(self):
		config_dict = {
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
			with open(self.json_file, mode='w', encoding='utf-8') as f:
				f.write(json.dumps(config_dict, indent=4, sort_keys=True))
		except Exception as e:
			logging.error(e)
			logging.warning('Could not save config.json file')
			return
