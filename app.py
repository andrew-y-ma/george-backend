import os
import re
from flask import Flask
from flask import request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

app = Flask(__name__)

URL = "https://www.walmart.ca/en/grocery/dairy-eggs/N-3798"
CHROME_DRIVER_PATH = os.path.abspath('./chromedriver_mac') #comment this line on windows

# CHROME_DRIVER_PATH = os.path.abspath('./chromedriver_windows.exe') # uncomment line on windows
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

@app.route('/')
def hello_world():
    return 'Hello, World!'

#testing endpoint
@app.route('/website', methods=['GET', 'POST'])
def upload_file():    
    grocery_items = query_prices()
    return grocery_items

# Obtains price data from Walmart eggs and dairy section at the moment 
def query_prices():
    driver.get(URL)
    f = open("website-content.html", "w") #creates local html file for testing purposes
    f.write(driver.page_source)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', class_='product-details-container')
    grocery_item_dict = {}

    for result in results:
        match = re.search(r'<h2 class="thumb-header">([^<]*)', str(result))
        item_name = match.group(1)
        match = re.search(r'data-bind="possibleRangedCurrencyText: { data: price, simpleFormatting: simpleFormatting } "><span>\$</span>([\d\.]*)', str(result))

        if match is not None:
            item_price = match.group(1)
            grocery_item_dict[item_name] = item_price

    return grocery_item_dict


