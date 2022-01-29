from selenium import webdriver

#### for running locally on my computer ####
# for running locally on my computer
# from selenium.webdriver import Edge, EdgeOptions
# from selenium.webdriver.common.by import By
############################################

from selenium import webdriver # for Heroku

import pandas as pd
from datetime import datetime
from time import localtime, strftime
from pymongo import MongoClient
import json
import sys
import os # for Heroku

#### for running locally on my computer ####
# options = EdgeOptions()
# options.use_chromium = True

# driver = Edge(options = options)
############################################

########## for Heroku######################
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
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


def scrape_current_occupancy(location_url):

    driver.get(BASE_URL + location_url)
    location = driver.find_element(By.CLASS_NAME, 'LocationName-geo').text
    current_occupancy = driver.find_element(By.CSS_SELECTOR, 'div.Core-capacityStatus.js-capacity-status.Core-capacityStatus').text

    current_date = datetime.now().date()
    current_date = current_date.strftime('%x')
    current_time = datetime.now().time()
    current_time = current_time.strftime('%I:%M %p')
    
    return str(current_date) + ',' + str(current_time) + ','+ str(location).title() + ',' + str(current_occupancy)

def write_current_occupancy_to_file(current_occupancy, output_file):
    
    f = open(output_file, 'a')
    f.write('\n' + current_occupancy)
    f.close()

def write_to_occupancy_df(current_occupancy, output_file):
    
    split_current_occupancy = current_occupancy.split(',')
    
    # occupancy_df = pd.DataFrame([split_current_occupancy], columns = header_ls)
    # print(occupancy_df)
    # occupancy_df = pd.read_csv(output_file)
    if os.path.exists(output_file) == True:
        occupancy_df = pd.read_csv(output_file)
        occupancy_df.loc[len(occupancy_df)] = split_current_occupancy
    
    else:
        header_ls = ['date', 'time', 'location', 'occupancy']
        occupancy_df = pd.DataFrame([split_current_occupancy], columns = header_ls)
    
    occupancy_df.to_csv(output_file, index = False, header = True)

def main():
     
    location = 'Woodside'
    location_url = location_url_dict.get(location)
    current_occupancy_level = scrape_current_occupancy(location_url)
    # write_to_occupancy_df(current_occupancy_level, 'current_occupancy.csv')
    write_to_occupancy_db(connect_to_database('config.json'), current_occupancy_level)

    location = 'Jackson Heights'
    location_url = location_url_dict.get(location)
    current_occupancy_level = scrape_current_occupancy(location_url)
    # write_to_occupancy_df(current_occupancy_level, 'current_occupancy.csv')
    write_to_occupancy_db(connect_to_database('config.json'), current_occupancy_level)

desired_start_time = '2:20'    
desired_end_time = '19:00'
while True:
    if (strftime("%H:%M", localtime() >= desired_start_time) or (strftime("%H:%M", localtime() <= desired_end_time))):
        main()    

# if __name__ == '__main__':
#     main()

# def get_current_occupancy(location):

#     # location = sys.argv[1]
#     location_url = location_url_dict.get(location)
#     current_occupancy_level = scrape_current_occupancy(location_url)
#     write_to_occupancy_db(connect_to_database('config.json'), current_occupancy_level)