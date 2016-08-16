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
		self.config.set_last_run((datetime.utcnow()-timedelta(hours=12)).isoformat())

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
		keyword_string = self._getKeywordString(parser.payload)
		self.assertEqual(keyword_string, 'donkey kong country, snes')
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchAnyKeywords(self):
		self.config.search_profile['categories'] = []
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = [
			{
				"clause": "any",
				"keywords": "fm towns, pc-8801, pc-9801, x68000, x68k"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		keyword_string = self._getKeywordString(parser.payload)
		self.assertEqual(keyword_string, '(fm towns, pc-8801, pc-9801, x68000, x68k)')
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchAllNotKeywords(self):
		self.config.search_profile['categories'] = []
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = [
			{
				"clause": "all",
				"keywords": "castlevania"
			},
			{
				"clause": "not",
				"keywords": "gba"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		keyword_string = self._getKeywordString(parser.payload)
		self.assertEqual(keyword_string, 'castlevania -(gba)')
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchAnyNotKeywords(self):
		self.config.search_profile['categories'] = []
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = [
			{
				"clause": "any",
				"keywords": "castlevania, mario, zelda"
			},
			{
				"clause": "not",
				"keywords": "gba"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		keyword_string = self._getKeywordString(parser.payload)
		self.assertEqual(keyword_string, '(castlevania, mario, zelda) -(gba)')
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])	

	def testSearchCategoryOnly(self):
		self.config.search_profile['categories'] = ['11189']
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = []
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		for i, category in enumerate(self.config.search_profile['categories']):
			category_string = self._getCategoryString(i, parser.payload)
			self.assertEqual(category_string, category)
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchCategoryKeywords(self):
		self.config.search_profile['categories'] = ['11189']
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = [ 
			{
				"clause": "all",
				"keywords": "amiga"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		for i, category in enumerate(self.config.search_profile['categories']):
			category_string = self._getCategoryString(i, parser.payload)
			self.assertEqual(category_string, category)
		keyword_string = self._getKeywordString(parser.payload)
		self.assertEqual(keyword_string, 'amiga')
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchCategoriesKeywords(self):
		self.config.search_profile['categories'] = ['11189', '1249']
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = [ 
			{
				"clause": "all",
				"keywords": "amiga"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		for i, category in enumerate(self.config.search_profile['categories']):
			category_string = self._getCategoryString(i, parser.payload)
			self.assertEqual(category_string, category)
		keyword_string = self._getKeywordString(parser.payload)
		self.assertEqual(keyword_string, 'amiga')
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchFilterKeywords(self):
		self.config.search_profile['categories'] = []
		self.config.search_profile['filters'] = [
			{
				"name": "MaxPrice",
				"value": "100"
			}
		]
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = [
			{
				"clause": "any",
				"keywords": "castlevania, mario"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		for i, item_filter in enumerate(self.config.search_profile['filters'], start=1):
			item_filter_dict = self._getItemFilterDict(i, parser.payload)
			self.assertEqual(item_filter_dict, item_filter)
		keyword_string = self._getKeywordString(parser.payload)
		self.assertEqual(keyword_string, '(castlevania, mario)')
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchFiltersKeywords(self):
		self.config.search_profile['categories'] = []
		self.config.search_profile['filters'] = [
			{
				"name": "MinPrice",
				"value": "10"
			},
			{
				"name": "MaxPrice",
				"value": "80"
			}
		]
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = [
			{
				"clause": "any",
				"keywords": "castlevania, mario"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		for i, item_filter in enumerate(self.config.search_profile['filters'], start=1):
			item_filter_dict = self._getItemFilterDict(i, parser.payload)
			self.assertEqual(item_filter_dict, item_filter)
		keyword_string = self._getKeywordString(parser.payload)
		self.assertEqual(keyword_string, '(castlevania, mario)')
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchFilterCategory(self):
		self.config.search_profile['categories'] = ['139973']
		self.config.search_profile['filters'] = [
			{
				"name": "MinPrice",
				"value": "100"
			}
		]
		self.config.search_profile['output_selectors'] = []
		self.config.search_profile['search_terms'] = []
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		for i, category in enumerate(self.config.search_profile['categories']):
			category_string = self._getCategoryString(i, parser.payload)
			self.assertEqual(category_string, category)
		for i, item_filter in enumerate(self.config.search_profile['filters'], start=1):
			item_filter_dict = self._getItemFilterDict(i, parser.payload)
			self.assertEqual(item_filter_dict, item_filter)
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchOutputSelectorKeywords(self):
		self.config.search_profile['categories'] = []
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = ['PictureURLLarge']
		self.config.search_profile['search_terms'] = [
			{
				"clause": "any",
				"keywords": "castlevania, mario"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		for i, output_selector in enumerate(self.config.search_profile['output_selectors']):
			output_selector_string = self._getOutputSelectorString(i, parser.payload)
			self.assertEqual(output_selector_string, output_selector)
		keyword_string = self._getKeywordString(parser.payload)
		self.assertEqual(keyword_string, '(castlevania, mario)')
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchOutputSelectorsKeywords(self):
		self.config.search_profile['categories'] = []
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = ['PictureURLLarge', 'PictureURLSuperSize']
		self.config.search_profile['search_terms'] = [
			{
				"clause": "any",
				"keywords": "castlevania, mario"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		for i, output_selector in enumerate(self.config.search_profile['output_selectors']):
			output_selector_string = self._getOutputSelectorString(i, parser.payload)
			self.assertEqual(output_selector_string, output_selector)
		keyword_string = self._getKeywordString(parser.payload)
		self.assertEqual(keyword_string, '(castlevania, mario)')
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchOutputSelectorCategory(self):
		self.config.search_profile['categories'] = ['139973']
		self.config.search_profile['filters'] = []
		self.config.search_profile['output_selectors'] = ['PictureURLLarge']
		self.config.search_profile['search_terms'] = []
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		for i, category in enumerate(self.config.search_profile['categories']):
			category_string = self._getCategoryString(i, parser.payload)
			self.assertEqual(category_string, category)
		for i, output_selector in enumerate(self.config.search_profile['output_selectors']):
			output_selector_string = self._getOutputSelectorString(i, parser.payload)
			self.assertEqual(output_selector_string, output_selector)
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def testSearchEverything(self):
		self.config.search_profile['categories'] = ['139973', '54968', '38583']
		self.config.search_profile['filters'] = [
			{
				"name": "MinPrice",
				"value": "10"
			},
			{
				"name": "MaxPrice",
				"value": "500"
			}
		]
		self.config.search_profile['output_selectors'] = ['PictureURLLarge', 'PictureURLSuperSize']
		self.config.search_profile['search_terms'] = [
			{
				"clause": "all",
				"keywords": "mario"
			},
			{
				"clause": "any",
				"keywords": "super, new, bros"
			},
			{
				"clause": "not",
				"keywords": "gba"
			}
		]
		parser = EbayParser(self.config)
		parser.make_payload()
		parser.make_request()
		parser.parse_response()
		for i, category in enumerate(self.config.search_profile['categories']):
			category_string = self._getCategoryString(i, parser.payload)
			self.assertEqual(category_string, category)
		for i, item_filter in enumerate(self.config.search_profile['filters'], start=1):
			item_filter_dict = self._getItemFilterDict(i, parser.payload)
			self.assertEqual(item_filter_dict, item_filter)
		for i, output_selector in enumerate(self.config.search_profile['output_selectors']):
			output_selector_string = self._getOutputSelectorString(i, parser.payload)
			self.assertEqual(output_selector_string, output_selector)
		keyword_string = self._getKeywordString(parser.payload)
		self.assertEqual(keyword_string, 'mario (super, new, bros) -(gba)')
		self.assertEqual(parser.response.status_code, 200)
		self.assertIsNotNone(parser.response.json()['findItemsAdvancedResponse'][0]['searchResult'])

	def _getKeywordString(self, payload):
		return next(param[1] for param in payload if param[0] == 'keywords')

	def _getCategoryString(self, i, payload):
		return next(param[1] for param in payload if param[0] == 'categoryId({!s})'.format(i))

	def _getItemFilterDict(self, i, payload):
		item_filter_dict = {
			"name": next(param[1] for param in payload if param[0] == 'itemFilter({!s}).name'.format(i)),
			"value": next(param[1] for param in payload if param[0] == 'itemFilter({!s}).value'.format(i))
		}
		return item_filter_dict

	def _getOutputSelectorString(self, i, payload):
		return next(param[1] for param in payload if param[0] == 'outputSelector({!s})'.format(i))
