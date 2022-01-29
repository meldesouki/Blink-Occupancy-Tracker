from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import time
from pymongo import MongoClient
import json
import os # for Heroku

############################################

########## for Heroku######################
ser = Service(os.environ.get("CHROMEDRIVER_PATH"))
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(service=ser, options=chrome_options)
###########################################


WOODSIDE_LOCATION_URL = 'ny/queens/56-02-roosevelt-avenue'
JACKSON_HEIGHTS_URL = 'ny/queens/78-14-roosevelt-avenue'
BASE_URL = 'https://locations.blinkfitness.com/'

location_url_dict = {

    'Woodside' : 'ny/queens/56-02-roosevelt-avenue',
    'Jackson Heights' : 'ny/queens/78-14-roosevelt-avenue'
}

def connect_to_database(config):
    
    with open(config) as json_config_file:
        credentials = json.load(json_config_file)
    
    username = credentials.get('user')
    password = credentials.get('password')

    client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.yuctu.mongodb.net/current_occupancy?retryWrites=true&w=majority')
    db = client.occupancy_tracker

    return db

def connect_to_database_no_config_file():
    
    username = os.environ.get("MONGODB_USER")
    password = os.environ.get("MONGODB_PASSWORD")

    client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.yuctu.mongodb.net/current_occupancy?retryWrites=true&w=majority')
    db = client.occupancy_tracker

    return db

def write_to_occupancy_db(db, current_occupancy):
    
    split_current_occupancy = current_occupancy.split(',')

    occupancy_log_entry = {
        'date' : split_current_occupancy[0],
        'time' : split_current_occupancy[1],
        'location': split_current_occupancy[2],
        'occupancy': split_current_occupancy[3]
    }

    result = db.current_occupancy.insert_one(occupancy_log_entry)
    print(f'Entry has been logged with ID: {result.inserted_id}')


def scrape_current_occupancy(location_url):

    driver.get(BASE_URL + location_url)
    location = driver.find_element(By.CLASS_NAME, 'LocationName-geo').text
    current_occupancy = driver.find_element(By.CSS_SELECTOR, 'div.Core-capacityStatus.js-capacity-status.Core-capacityStatus').text

    current_date = datetime.now().date()
    current_date = current_date.strftime('%x')
    current_time = datetime.now().time()
    current_time = current_time.strftime('%I:%M %p')
    
    return str(current_date) + ',' + str(current_time) + ','+ str(location).title() + ',' + str(current_occupancy)

def write_to_occupancy_df(current_occupancy, output_file):
    
    split_current_occupancy = current_occupancy.split(',')
    
    if os.path.exists(output_file) == True:
        occupancy_df = pd.read_csv(output_file)
        occupancy_df.loc[len(occupancy_df)] = split_current_occupancy
    
    else:
        header_ls = ['date', 'time', 'location', 'occupancy']
        occupancy_df = pd.DataFrame([split_current_occupancy], columns = header_ls)
    
    occupancy_df.to_csv(output_file, index = False, header = True)


desired_start_time = datetime.strptime('07:00', '%H:%M')    
desired_end_time = datetime.strptime('19:00', '%H:%M') 
 
while True:
    
    print("code should run soon")
    
    if (desired_start_time <= datetime.now() <= desired_end_time ):
        
        print("code is running")
        location = 'Woodside'
        location_url = location_url_dict.get(location)
        current_occupancy_level = scrape_current_occupancy(location_url)
        write_to_occupancy_db(connect_to_database_no_config_file(), current_occupancy_level)

        location = 'Jackson Heights'
        location_url = location_url_dict.get(location)
        current_occupancy_level = scrape_current_occupancy(location_url)
        write_to_occupancy_db(connect_to_database_no_config_file(), current_occupancy_level)
        time.sleep(3600) # runs every hour 
