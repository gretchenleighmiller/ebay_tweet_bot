eBay Tweet Bot
==============

eBay Tweet Bot is a simple program that posts results from an eBay search to Twitter.

The bot is configured to take a JSON file with the following:
- An eBay API app ID.
- Twitter API credentials (Consumer API Key and Access Token for a specific Twitter account).
- A Bitly access token (for shortening the REALLY long eBay URIs).
- An eBay search profile.

JSON Config
-----------
- ebay_api_app_id: Your eBay API App ID.
- bitly_access_token: Your Bitly acess token.
- twitter_api_config: Twitter API credentials.
- twitter_api_config.access_token_key: Your Twitter Access Token Key.
- twitter_api_config.access_token_secret: Your Twitter Access Token Secret.
- twitter_api_config.consumer_key: Your Twitter Consumer API key.
- twitter_api_config.consumer_secret: Your Twitter Consumer API secret.
- search_profile: The eBay search profile.
- search_profile.categories: A JSON array of up to three eBay Categories.
- search_profile.filters: A JSON array of JSON objects with "name" and "value" keys for each filter.
- search_profile.output_selectors: A JSON array of output selectors.
- search_profile.search_terms: A JSON array of JSON objects with "clause" and "keywords" keys. Allowed clauses are "all", "any", and "not". Keywords must be comma-separated.
last_run: An ISO 8601 timestamp representing the last time the bot was run. This will be updated automatically after the initial run.

For an eBay search you must have either one category or one search term.

See config.sample.json for an config.

Using the Bot
-------------
Once you've set up the configuration, the run.py script in the base directory will look for new listings since the last_run timestamp, post the new listings to Twitter, and finally update and save the config.json file with the updated last_run timestamp.

I suggest using cron to run the bot on a schedule, but it can also be run manually or via another scheduling tool.

There is logging to ebay_twitterbot.log in the base directory.

eBay Categories Report
----------------------
Getting all the eBay Categories can be a bit of a pain. I created a simple script located in the base directory, ebay_categories_report.py, that will generate a text list of all eBay categories, with tabbing to represent hierarchical depth.



