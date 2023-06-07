from Scrapers import *

scrapers = [SampathBankScraper(), CommBankScraper(), SeylanBankScraper()]

for scraper in scrapers:
		scraper.scrape()
		scraper.debug_out()