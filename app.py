from flask import Flask
from flask import request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os

app = Flask(__name__)

URL = "https://www.walmart.ca/en/grocery/dairy-eggs/N-3798"
CHROME_DRIVER_PATH = os.path.abspath('./chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(URL)

page = requests.get(URL)
#Get HTML associated with URL
# URL = "https://www.monster.com/jobs/search/?q=Software-Developer&where=Australia"

@app.route('/')
def hello_world():
    return 'Hello, World!'

#testing endpoint
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return {
            "hi": request.args.get('testing'),
            "bye": "asdfl;kjzxcbl;"
        }
    
    f = open("website-content.html", "w")
    encoding = 'utf-8'
    
    f.write(driver.page_source)

    # f.write(page.content.decode(encoding))
    print(page.content)
    print(CHROME_DRIVER_PATH)
    print(driver.page_source)
    print('printed request')
    return 'Get request for this endpoint'


# #endpoint for webscraping testing yee yee
# @app.route('/website', methods=['GET', 'POST'])
# def yeet():
#     save_html(r.content, )
#     if request.method == 'POST':
#         return {
#             "hi": request.args.get('testing'),
#             "bye": "asdfl;kjzxcbl;"
#         }
#     return 'Get request for this endpoint!'


# def save_html(html, path):
#     with open(path, 'wb') as f:
#         f.write(html)

    