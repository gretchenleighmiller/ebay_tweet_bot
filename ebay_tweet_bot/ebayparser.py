# -*- coding: utf-8 -*-
import requests

class EbayParser():

	FINDING_BASE_URL = 'http://svcs.ebay.com/services/search/FindingService/v1'
	SERVICE_VERSION = '1.0.0'
	OPERATION_NAME = 'findItemsAdvanced'
	RESPONSE_FORMAT = 'JSON'

	def __init__(self, config):
		# using a list of tuples instead of a dict because eBay API is VERY sensitive about parameter order
		self.payload = [
			('OPERATION-NAME', self.OPERATION_NAME),
			('SERVICE-VERISON', self.SERVICE_VERSION),
			('SECURITY-APPNAME', config.ebay_api_app_id),
			('RESPONSE-DATA-FORMAT', self.RESPONSE_FORMAT),
			('REST-PAYLOAD', 'true')
		]
		self.search_profile = config.search_profile
		self.start_time_from = config.last_run
		self.response = None
		self.listings = []

	def make_payload(self):
		categories = self.search_profile['categories']
		filters = self.search_profile['filters']
		output_selectors = self.search_profile['output_selectors']
		search_terms = self.search_profile['search_terms']
		keywords = ''
		# multiple parameters of the same type are differentiated by a 0-indexed counter
		for i, category in enumerate(categories):
			self.payload.append(('categoryId({!s})'.format(i), category))
		self.payload.append(('itemFilter(0).name', 'StartTimeFrom'))
		self.payload.append(('itemFilter(0).value', self.start_time_from))
		for i, item_filter in enumerate(filters, start=1):
			self.payload.append(('itemFilter({!s}).name'.format(i), item_filter['name']))
			self.payload.append(('itemFilter({!s}).value'.format(i), item_filter['value']))
		for i, output_selector in enumerate(output_selectors):
			self.payload.append(('outputSelector({!s})'.format(i), output_selector))
		for search_term in search_terms:
			if search_term['clause']=='all':
				keywords += search_term['keywords']
			if search_term['clause']=='any':
				keywords += '({})'.format(search_term['keywords'])
			if search_term['clause']=='not':
				keywords += '-({})'.format(search_term['keywords'])
			keywords += ' '
		self.payload.append(('keywords', keywords.strip()))

	def make_request(self):
		self.response = requests.get(self.FINDING_BASE_URL, params=self.payload)

	def parse_response(self):
		if self.response.json()['findItemsAdvancedResponse'][0]['searchResult'][0]['@count']!='0':
			raw_listings = self.response.json()['findItemsAdvancedResponse'][0]['searchResult'][0]['item']
		else:
			return
		for raw_listing in raw_listings:
			title = raw_listing['title'][0]
			price = raw_listing['sellingStatus'][0]['convertedCurrentPrice'][0]['__value__']
			if 'pictureURLSuperSize' in raw_listing:
				image_url = raw_listing['pictureURLSuperSize'][0]
			elif 'pictureURLLarge' in raw_listing:
				image_url = raw_listing['pictureURLLarge'][0]
			elif 'galleryURL' in raw_listing:
				image_url = raw_listing['galleryURL'][0]
			else:
				image_url = None
			item_url = raw_listing['viewItemURL'][0]
			self.listings.append((title, price, image_url, item_url))

