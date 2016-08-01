# -*- coding: utf-8 -*-
import twitter

class Tweeter():
	def __init__(self, config_consumer_key, config_consumer_secret, config_access_token_key, config_access_token_secret):
		self.api = twitter.Api( consumer_key=config_consumer_key,
								consumer_secret=config_consumer_secret,
								access_token_key=config_access_token_key,
								access_token_secret=config_access_token_secret,
								sleep_on_rate_limit=True)


	def send_tweet(self, listing):
		title, price, image_url = listing
		message = '%s – %s' % (title, price)
		self.api.PostUpdate(message, media=image_url)
