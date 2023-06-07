import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Path to ChromeDriver executable
webdriver_path = "/home/meth/chromedriver/stable/chromedriver"

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

class SampathBankScraper(CurrencyScraper):
	def __init__(self, url=""):
		super().__init__("https://www.sampath.lk/rates-and-charges?activeTab=exchange-rates")
		self.__initialize_selenium()
		
		# Navigate to webpage
		self.s_driver.get(self.url)

	def __initialize_selenium(self):
		self.s_service = Service(webdriver_path)
		self.s_options = webdriver.ChromeOptions()
		self.s_options.add_argument("--headless")
		self.s_driver = webdriver.Chrome(service=self.s_service, options=self.s_options)
	
	def scrape(self):
		the_table = self.s_driver.find_element(By.ID, "__BVID__413")
		rows = the_table.find_elements(By.TAG_NAME, "tbody")

		for row in rows:
			cell_row = row.find_element(By.TAG_NAME, "tr")
			cells = cell_row.find_elements(By.TAG_NAME, "td")
			text = [cell.get_attribute("innerHTML").strip() for cell in cells]
			print(text)