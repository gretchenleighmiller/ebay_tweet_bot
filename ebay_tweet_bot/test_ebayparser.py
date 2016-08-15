# -*- coding: utf-8 -*-

import sys, os, unittest
from datetime import datetime, timedelta
from ebay_tweet_bot import Config, EbayParser

class EbayParserTester(unittest.TestCase):
	def setUp(self):
		self.dir_path = os.path.dirname(sys.argv[0])
		self.dir_path = os.path.join(self.dir_path, 'test_data')
		self.config_file_path = os.path.join(self.dir_path, 'test_config.json')
		self.config = Config(self.config_file_path)
		self.config.last_run = (datetime.utcnow()-timedelta(hours=12)).isoformat()

	def testSearchAllKeywords(self):
		self.config.search_profile['categories'] = []
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = [ 
			{
				"clause": "all",
				"keywords": "donkey kong country, snes"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchAnyKeywords(self):
		pass

	def testSearchAllNotKeywords(self):
		pass

	def testSearchAnyNotKeywords(self):
		pass

	def testSearchCategoryOnly(self):
		pass

	def testSearchCategoryKeywords(self):
		self.config.search_profile['categories'] = ['11189']
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = [ 
			{
				"clause": "any",
				"keywords": "amiga"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchCategoriesKeywords(self):
		self.config.search_profile['categories'] = ['11189', '1249']
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = [ 
			{
				"clause": "any",
				"keywords": "amiga"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchFilterKeywords(self):
		pass

	def testSearchFiltersKeywords(self):
		pass

	def testSearchFilterCategory(self):
		pass
