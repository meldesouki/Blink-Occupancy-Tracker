from selenium import webdriver
import selenium
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

options = EdgeOptions()
options.use_chromium = True

driver = Edge(options = options)


WOODSIDE_LOCATION_URL = 'ny/queens/56-02-roosevelt-avenue'
JACKSON_HEIGHTS_URL = 'ny/queens/78-14-roosevelt-avenue'
BASE_URL = 'https://locations.blinkfitness.com/'


headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'
req = driver.get(BASE_URL + WOODSIDE_LOCATION_URL)
# current_occupancy = driver.find_element_by_css_selector('div.Core-capacityStatus.js-capacity-status.Core-capacityStatus--green')
# html_doc = req.content
# soup = BeautifulSoup(req.page_source, 'html.parser')

# print(soup)
# current_occupancy = soup.find('div', class_ = 'Core-capacityStatus js-capacity-status Core-capacityStatus--green')

current_occupancy = driver.find_element(By.CSS_SELECTOR, 'div.Core-capacityStatus.js-capacity-status.Core-capacityStatus--green')
f = open('current_occupancy.txt', 'a')
f.write('\n' + current_occupancy.text)
f.close()
