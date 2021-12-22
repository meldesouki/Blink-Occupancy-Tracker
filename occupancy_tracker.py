import requests
from bs4 import BeautifulSoup


WOODSIDE_LOCATION_URL = 'ny/queens/56-02-roosevelt-avenue'
JACKSON_HEIGHTS_URL = 'ny/queens/78-14-roosevelt-avenue'
BASE_URL = 'https://locations.blinkfitness.com/'


headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'
req = requests.get(BASE_URL + WOODSIDE_LOCATION_URL, headers = headers)
html_doc = req.content
soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup)
current_occupancy = soup.find('div', class_ = 'Core-capacityStatus js-capacity-status Core-capacityStatus--green')

print(current_occupancy.text)
