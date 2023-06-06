from Scrapers import *

cbs = CommBankScraper()
cbs.scrape()

sbs = SeylanBankScraper()
sbs.scrape()

cbs.debug_out()
sbs.debug_out()