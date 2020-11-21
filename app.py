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
driver.get(URL)

@app.route('/')
def hello_world():
    return 'Hello, World!'

#testing endpoint
@app.route('/website', methods=['GET', 'POST'])
def upload_file():
    # if request.method == 'POST':
    #     return {
    #         "hi": request.args.get('testing'),
    #         "bye": "asdfl;kjzxcbl;"
    #     }
    
    grocery_items = query_prices()
    return grocery_items

def query_prices():
    f = open("website-content.html", "w")
    f.write(driver.page_source)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', class_='product-details-container')
    grocery_item_dict = {}

    for result in results:
        match = re.search(r'<h2 class="thumb-header">([^<]*)', str(result))
        item_name = match.group(1)
        match = re.search(r'<span>\$</span>([\d\.]*)', str(result))

        if match is not None:
            item_price = match.group(1)
            grocery_item_dict[item_name] = item_price

    grocery_prices = soup.find_all('span', class_='product-price-analytics')
    return grocery_item_dict

