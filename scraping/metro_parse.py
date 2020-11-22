from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://www.metro.ca'

def get_metro_products(item_name):
    item_name.replace(' ', '+')

    URL_ENDPOINT = 'https://www.metro.ca/en/online-grocery/search?filter=' + item_name + '&freeText=true'

    page = requests.get(URL_ENDPOINT)
    soup = BeautifulSoup(page.content, 'html.parser')

    tiles = soup.find_all('div', {'class': "products-tile-list__tile"})

    products = []
    for item in tiles:
        name = item.find('div', {'class': "pt-title"}).contents[0]
        price = item.find('div', {'class': "pi--main-price"}).div.span.contents[0]
        link = item.find('a', {'class': "pt--image product-details-link"})
        products.append({
            'name': name,
            'price': price,
            'link': BASE_URL + link['href']
        })
    
    return products

if __name__ == "__main__":
    item_name = input('Name of item to search: ')

    print(get_metro_products(item_name))
