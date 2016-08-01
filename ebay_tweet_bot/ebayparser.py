# -*- coding: utf-8 -*-
import requests

class EbayParser():

	FINDING_BASE_URL = 'http://svcs.ebay.com/services/search/FindingService/v1'
	SERVICE_VERSION = '1.0.0'
	OPERATION_NAME = 'findItemsAdvanced'
	RESPONSE_FORMAT = 'JSON'

	def __init__(self, config):
		
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
		filters = self.search_profile['filters']
		search_terms = self.search_profile['search_terms']
		output_selectors = self.search_profile['output_selectors']
		keywords = ''
		self.payload.append(('categoryId', self.search_profile['category']))
		self.payload.append(('itemFilter(0).name', 'StartTimeFrom'))
		self.payload.append(('itemFilter(0).value', self.start_time_from))
		for i, item_filter in enumerate(filters):
			self.payload.append(('itemFilter(' + str(i + 1) + ').name', item_filter['name']))
			self.payload.append(('itemFilter(' + str(i + 1) + ').value',item_filter['value']))
		for output_selector in output_selectors:
			self.payload.append(('outputSelector', output_selector))
		
		for search_term in search_terms:
			if search_term['clause']=='all':
				keywords += search_term['keywords']
			if search_term['clause']=='any':
				keywords += '(%s)' % (search_term['keywords'])
			if search_term['clause']=='not':
				keywords += '-(%s)' % (search_term['keywords'])
			keywords += ' '
		self.payload.append(('keywords', keywords.strip()))

	def make_request(self):
		self.response = requests.get(self.FINDING_BASE_URL, params=self.payload)

	def parse_response(self):
		raw_listings = self.response.json()['findItemsAdvancedResponse'][0]['searchResult'][0]['item']
		for raw_listing in raw_listings:
			title = raw_listing['title'][0]
			price = raw_listing['sellingStatus'][0]['convertedCurrentPrice'][0]['__value__']
			image_url = raw_listing['pictureURLLarge'][0]
			self.listings.append((title, price, image_url))

