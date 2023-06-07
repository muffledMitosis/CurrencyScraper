import requests
from bs4 import BeautifulSoup

from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Path to ChromeDriver executable
webdriver_path = "/home/meth/chromedriver/stable/chromedriver"

@dataclass
class SeleniumConfig:
	service: Service
	options: webdriver.ChromeOptions

class CurrencyScraper:
	def __init__(self, url="", readsite=True):
		self.url = url
		self.currencyList = []

		# raw data format -> [iso4217, buying, selling]
		self.raw_data = []

		self.resp = None
		self.soup = None
		
		# Don't send request if using selenium
		if readsite:
			self.__readSite()					# TODO: Implement caching. Dont wanna overload servers
	
	def __readSite(self):
		self.resp = requests.get(self.url)
		self.soup = BeautifulSoup(self.resp.content, "html.parser")
	
	# Print raw data that has been scraped
	def debug_out(self):
		for row in self.raw_data:
			print(row)

class CommBankScraper(CurrencyScraper):
	def __init__(self):
		super().__init__("https://www.combank.lk/rates-tariff")

	def scrape(self):
		print("Scraping from " + self.url)

		exchange_rates_div = self.soup.find("div", id="exchange-rates")
		table = exchange_rates_div.find("table")
		rows = table.find_all("tr")
		rows = rows[3:]						# Remove garbage rows

		for row in rows:
			cells = row.find_all("td")
			first_three_columns = [cell.text.strip() for cell in cells[:3]]
			self.raw_data.append(first_three_columns)

class SeylanBankScraper(CurrencyScraper):
	def __init__(self):
		super().__init__("https://www.seylan.lk/exchange-rates")

	def scrape(self):
		print("Scraping from " + self.url)

		table = self.soup.find("table", class_="table-style-4")
		rows = table.find_all("tr")
		rows = rows[2:]						# Remove garbage rows

		for row in rows:
			cells = row.find_all("td")
			first_three = [cell.text.strip() for cell in cells[1:4]]
			self.raw_data.append(first_three)

class SampathBankScraper(CurrencyScraper):
	def __init__(self):
		super().__init__("https://www.sampath.lk/rates-and-charges?activeTab=exchange-rates", readsite=False)
		# TODO: Implement caching for selenium and nav
		self.__initialize_selenium()
		
		# Navigate to webpage
		self.selenium_driver.get(self.url)

	def __initialize_selenium(self):
		self.selenium_config = SeleniumConfig(
			Service(webdriver_path),
			webdriver.ChromeOptions(),
		)

		self.selenium_config.options.add_argument("--headless")

		self.selenium_driver = webdriver.Chrome(service=self.selenium_config.service,
		    options=self.selenium_config.options
		)
	
	def scrape(self):
		the_table = self.selenium_driver.find_element(By.ID, "__BVID__413")
		rows = the_table.find_elements(By.TAG_NAME, "tbody")

		for row in rows:
			# Get the actuall data
			cell_row = row.find_element(By.TAG_NAME, "tr")
			cells = cell_row.find_elements(By.TAG_NAME, "td")
			
			# Drop what we don't need
			text = [cell.get_attribute("innerHTML").strip() for cell in cells]
			text = [text[0], text[2], text[4]]

			self.raw_data.append(text)