# -*- coding: utf-8 -*-
import json
from datetime import datetime

class Config():
	def __init__(self, json_file):
		self.json_file = json_file
		self.ebay_api_app_id = None
		self.finding_base_url = None
		self.service_version = None
		self.search_profile = {}
		self.twitter_consumer_key = None
		self.twitter_consumer_secret = None
		self.twitter_access_token_key = None
		self.twitter_access_token_secret = None
		self.last_run = None
		self.load_config()

	def load_config(self):
		config_dict = {}

		with open(self.json_file, mode='r', encoding='utf-8') as f:
			config_dict = json.load(f)
			
		self.ebay_api_app_id = config_dict['ebay_api_config']['app_id']
		self.finding_base_url = config_dict['ebay_api_config']['finding_base_url']
		self.service_version = config_dict['ebay_api_config']['service_version']
		self.search_profile = config_dict['search_profile']
		self.twitter_consumer_key = config_dict['twitter_api_config']['consumer_key']
		self.twitter_consumer_secret = config_dict['twitter_api_config']['consumer_secret']
		self.twitter_access_token_key = config_dict['twitter_api_config']['access_token_key']
		self.twitter_access_token_secret = config_dict['twitter_api_config']['access_token_secret']
		self.last_run = config_dict['last_run']

	def set_last_run(self):
		self.last_run = datetime.utcnow().isoformat()

	def save_config(self):
		config_dict = {
			'ebay_api_config': {
				'app_id': self.ebay_api_app_id,
				'finding_base_url': self.finding_base_url,
				'service_version': self.service_version
			},
			'search_profile': self.search_profile,
			'twitter_api_config': {
				'consumer_key': self.twitter_consumer_key,
				'consumer_secret': self.twitter_consumer_secret,
				'access_token_key': self.twitter_access_token_key,
				'access_token_secret': self.twitter_access_token_secret
			},
			'last_run': self.last_run
		}

		with open(self.json_file, mode='w', encoding='utf-8') as f:
			f.write(json.dumps(config_dict, indent=4, sort_keys=True))
