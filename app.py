import os
import re
import sys
import os.path
sys.path.append(os.path.join(os.path.abspath(__file__), '..'))
from scraping.metro_parse import get_metro_products

from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

app = Flask(__name__)

URL = "https://www.walmart.ca/en/grocery/dairy-eggs/N-3798"
BASE_URL = "https://www.walmart.ca/"
URL_ENDPOINT = "https://www.walmart.ca/search?q="
CHROME_DRIVER_PATH = os.path.abspath('./chromedriver_mac') if sys.platform == 'darwin' \
    else os.path.abspath('./chromedriver_windows.exe')

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

# search_qeury = "gala%20apples"
# url = BASE_URL + "?q=" + search_qeury + "&c=10019"
# driver.get(url)

@app.route('/')
def hello_world():
    response = jsonify({'data': 'Hello, world!'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#testing endpoint
@app.route('/website', methods=['GET', 'POST'])
def upload_file():    

    query = request.args.get('q')
    print(query)
    grocery_items = query_prices_walmart_search(query)
    return grocery_items

@app.route('/products')
def return_product_list():
    item_name = request.args.get('item_name')
    response = jsonify(get_metro_products(item_name))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Obtains price data from Walmart eggs and dairy section at the moment 
def query_prices_walmart():
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


# Obtains price data from term that is serached up
def query_prices_walmart_search(search_qeury):
    url = URL_ENDPOINT + search_qeury + "&c=10019"
    driver.get(url)

    # driver.get(url)
    f = open("website-content.html", "w") #creates local html file for testing purposes
    f.write(driver.page_source)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', class_='css-vh2dix e1m8uw910')
    grocery_item_dict = {}

    for result in results:
        name = result.find('p', {'data-automation': 'name'}).text
        href = result.find('a', class_="css-n8po8v e1m8uw911").attrs['href']
        price = result.find('span', {'data-automation': 'current-price'})
        print(price)

        if "¢" in price.text:
            price = price.text
            price = "0." + price
        else:
            price = price.text

        grocery_item_dict[name] = {
            'price': price,
            'href': BASE_URL + href 
        }

    return grocery_item_dict

    #alternative approaches:
    # takes in list of inputs 