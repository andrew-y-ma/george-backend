from bs4 import BeautifulSoup
import requests

item_name = input('Name of item to search: ')
item_name.replace(' ', '+')

BASE_URL = 'https://www.metro.ca'
URL_ENDPOINT = 'https://www.metro.ca/en/online-grocery/search?filter=' + item_name + '&freeText=true'

page = requests.get(URL_ENDPOINT)
soup = BeautifulSoup(page.content, 'html.parser')

tiles = soup.find_all('div', {'class': "products-tile-list__tile"})

products = {}
for ite in tiles:
    name = ite.find('div', {'class': "pt-title"}).contents[0]
    price = ite.find('div', {'class': "pi--main-price"}).div.span.contents[0]
    link = ite.find('a', {'class': "pt--image product-details-link"})
    products[name] = {
        'price': price,
        'link': BASE_URL + link['href']
    }

print(products)
