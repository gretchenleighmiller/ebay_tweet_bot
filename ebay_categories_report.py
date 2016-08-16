# -*- coding: utf-8 -*-
import requests
from ebay_tweet_bot import Config

SHOPPING_BASE_URL = 'http://open.api.ebay.com/shopping'

def main():
	config = Config('config.json')

	payload = {
			'callname': 'GetCategoryInfo',
			'responseencoding': 'JSON',
			'appid': config.ebay_api_app_id,
			'siteid': '0',
			'version': '963',
			'IncludeSelector': 'ChildCategories'
		}
	
	report = recurse_ebay_categories_from_api(payload)

	with open('ebay_categories_report.txt', mode='w', encoding='utf-8') as f:
		f.write(report)

def recurse_ebay_categories_from_api(payload, report='EBAY CATEGORY REPORT \n', parent_id=None, categories=None):
	if categories is None:
		categories = get_root_ebay_category()
		parent_id = categories[0]['CategoryID']
	payload['CategoryID'] = parent_id
	results = requests.get(SHOPPING_BASE_URL, params=payload)
	results = results.json()['CategoryArray']['Category']
	results.pop(0)
	for result in results:
		print(result['CategoryName'])
		tabs = '\t' * result['CategoryLevel']
		report += '{0}{1} ({2})\n'.format(tabs, result['CategoryName'], result['CategoryID'])
		if result['LeafCategory'] is False:
			report = recurse_ebay_categories_from_api(payload, report, result['CategoryID'], categories)
	return report

def get_root_ebay_category():
	categories = []
	root_category = {
		'CategoryID': '-1',
		'CategoryName': 'Root',
		'LeafCategory': False,
		'CategoryParentID': '0',
		'CategoryLevel': 0
	}
	categories.append(root_category)
	return categories

if __name__ == '__main__':
	main()