# Random-URLs (NOT: Random URLs ;) ) for comics which have a website based random functionality
comics = [	'https://c.xkcd.com/random/comic/',
			'http://www.commitstrip.com/?random=1',
			'https://satwcomic.com/random']
		
# URLs for comics which do not have a website based random functionality and therefore need a scraper module in Modules/ComicScraper.py
# Note: Comics in this List without a scraper in Modules/ComicScraper.py will not be scraped and return a No-Scraper-Info in IRC.
#       If you want to add a comic website here then you will probably have to add scraping functionality to the ComicScraper for it.
scraper_comics =[ 	'http://betamonkeys.co.uk/category/comics/feed/']