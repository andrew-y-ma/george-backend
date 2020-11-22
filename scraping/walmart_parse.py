from bs4 import BeautifulSoup
import requests

item_name = input('Name of item to search: ')
item_name.replace(' ', '%20')

BASE_URL = 'https://www.walmart.ca/'
URL_ENDPOINT = 'https://www.walmart.ca/search?q=' + item_name

page = requests.get(URL_ENDPOINT)
soup = BeautifulSoup(page.content, 'html.parser')

tiles = soup.find_all('div', {'data-automation': "product"})
tiles.pop(0)
# print(tiles[1])

products = {}
for ite in tiles:
    print(ite)
    name = ite.find('p', {'data-automation': "name"}).contents[0]
    price = soup.find('span', {'data-automation': "current-price"})
    link = ite.find('a')
    products[name] = {
        'price': price,
        'link': BASE_URL + link['href']
    }

print(products)
