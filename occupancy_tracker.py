from os import fsdecode
from selenium import webdriver
import selenium
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime


options = EdgeOptions()
options.use_chromium = True

driver = Edge(options = options)

WOODSIDE_LOCATION_URL = 'ny/queens/56-02-roosevelt-avenue'
JACKSON_HEIGHTS_URL = 'ny/queens/78-14-roosevelt-avenue'
BASE_URL = 'https://locations.blinkfitness.com/'

def scrape_current_occupancy(location_url):

    driver.get(BASE_URL + location_url)
    location = driver.find_element(By.CLASS_NAME, 'LocationName-geo').text
    current_occupancy = driver.find_element(By.CSS_SELECTOR, 'div.Core-capacityStatus.js-capacity-status.Core-capacityStatus--green').text

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
    # occupancy_df = pd.DataFrame([split_current_occupancy])
    # print(occupancy_df)
    occupancy_df = pd.read_csv(output_file)
    occupancy_df.loc[len(occupancy_df)] = split_current_occupancy
    occupancy_df.to_csv(output_file, index = False, header = False)

def main():

    print('Choose a location:')
    print('1 - Woodside     2 - Jackson Heights')
    location = int(input())
    
    while (location != 1) and (location != 2):
        print('You made an invalid choice. Try again')
        location = int(input())

    if (location == 1):

        location_url = WOODSIDE_LOCATION_URL

    elif (location == 2):

        location_url = JACKSON_HEIGHTS_URL 
    
    current_occupancy_level = scrape_current_occupancy(location_url)
    # write_current_occupancy_to_file(current_occupancy_level,'current_occupancy.txt')
    write_to_occupancy_df(current_occupancy_level, 'current_occupancy.csv')
    

if __name__ == '__main__':
    main()