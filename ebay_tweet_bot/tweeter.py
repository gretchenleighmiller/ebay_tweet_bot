# -*- coding: utf-8 -*-
import twitter
import requests

class Tweeter():
	
	BITLY_API_BASE_URL = 'https://api-ssl.bitly.com/v3/shorten'

	def __init__(self, config_consumer_key, config_consumer_secret, config_access_token_key, config_access_token_secret, config_bitly_access_token):
		self.api = twitter.Api( consumer_key=config_consumer_key,
								consumer_secret=config_consumer_secret,
								access_token_key=config_access_token_key,
								access_token_secret=config_access_token_secret,
								sleep_on_rate_limit=True)
		self.bitly_access_token = config_bitly_access_token


	def send_tweet(self, listing):
		title, price, image_url, item_url = listing
		price = float(price)
		bitly_params = {
			'access_token': self.bitly_access_token,
			'longUrl': item_url,
			'format': 'txt'
		}
		if len(title) > 60:
			title = title[:57] + '...'
		short_item_url = requests.get(self.BITLY_API_BASE_URL, params=bitly_params).text
		message = '%s – $%.2f %s' % (title, price, short_item_url)
		if item_url:
			return self.api.PostUpdate(message, media=image_url)
		else:
			return self.api.PostUpdate(message)
