from bs4 import BeautifulSoup
import requests


def get_tnt_products(item_name):
    item_name.replace(' ', '+')
    item_name.replace('%20', '+')

    URL_ENDPOINT = 'https://www.tntsupermarket.com/catalogsearch/result/?q=' + item_name

    page = requests.get(URL_ENDPOINT)
    soup = BeautifulSoup(page.content, 'html.parser')

    tiles = soup.find_all('li', {'class': "item product product-item"})

    products = []
    for item in tiles:
        name = item.find('a', {'class': "product-item-link"}).contents[0]
        # print(item)

        special_price = item.find('span', {'class': "special-price"})

        if len(special_price) == 1:
            price = special_price.contents[0]
        else:
            price = item.find('span', {'class': "price"}).contents[0]

        link = item.find('a', {'class': "product-item-link"})['href']
        image = item.find('img')['src']

        products.append({
            'name': name,
            'price': price,
            'link': link,
            'image': image
        })
    
    return_product = products.pop(0)
    while '$' not in return_product['price'] and len(products) > 0:
        return_product = products.pop(0)

    return return_product

if __name__ == "__main__":
    item_name = input('Name of item to search: ')

    print(get_tnt_products(item_name))
