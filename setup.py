# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

dir_path = path.abspath(path.dirname(__file__))

with open(path.join(dir_path, 'README.rst'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='ebay_tweet_bot',
	version='1.0.0',
	description='eBay Tweet Bot is a simple program that posts results from an eBay search to Twitter',
	long_description=long_description,
	url='https://github.com/geoffsmiller/ebay_tweet_bot',
	author='Geoff Miller',
	author_email='geoffrey.s.miller@gmail.com',
	license='MIT',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Topic :: Internet :: WWW/HTTP'
	],
	keywords='twitter,bot,ebay,api',
	packages=find_packages(),
	install_requires=[
		'future>=0.15.2',
		'oauthlib>=1.1.2',
		'python-twitter>=3.1',
		'requests>=2.10.0',
		'requests-oauthlib>=0.6.2'
	]
)