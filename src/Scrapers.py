import requests
from bs4 import BeautifulSoup

class CurrencyScraper:
	def __init__(self, url=""):
		self.url = url
		self.currencyList = []
		self.resp = None
		self.soup = None
		self.__readSite()					# TODO: Implement caching. Dont wanna overload servers
	
	def __readSite(self):
		self.resp = requests.get(self.url)
		self.soup = BeautifulSoup(self.resp.content, "html.parser")
	
	# Print raw data that has been scraped
	def debug_out(self):
		for row in self.raw_data:
			print(row)

class CommBankScraper(CurrencyScraper):
	def __init__(self, url=""):
		super().__init__("https://www.combank.lk/rates-tariff")

	def scrape(self):
		print("Scraping from " + self.url)

		exchange_rates_div = self.soup.find("div", id="exchange-rates")
		table = exchange_rates_div.find("table")
		rows = table.find_all("tr")
		rows = rows[3:]						# Remove garbage rows

		self.raw_data = []

		for row in rows:
			cells = row.find_all("td")
			first_three_columns = [cell.text.strip() for cell in cells[:3]]
			self.raw_data.append(first_three_columns)

class SeylanBankScraper(CurrencyScraper):
	def __init__(self, url=""):
		super().__init__("https://www.seylan.lk/exchange-rates")

	def scrape(self):
		print("Scraping from " + self.url)

		table = self.soup.find("table", class_="table-style-4")
		rows = table.find_all("tr")
		rows = rows[2:]						# Remove garbage rows

		self.raw_data = []

		for row in rows:
			cells = row.find_all("td")
			first_three = [cell.text.strip() for cell in cells[1:4]]
			self.raw_data.append(first_three)