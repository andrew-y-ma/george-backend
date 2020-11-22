import requests

def make_pc_api_request(store_name, product): 

    BASE_URL = 'https://api.pcexpress.ca/marketplace/v2/banners/' + store_name + '/products?'

    product.replace(' ', '+')
    url_endpoint = BASE_URL + 'query=' + product + '&pageSize=48&pageNumber=1&sorts=relevance'

    query = requests.get(url_endpoint)
    print(query.status_code)
    response = query.json() if query.status_code == 200 else None

    if response == None:
        return

    product_results = response["results"]

    products = {}
    for product in product_results:
        name = product["title"]
        price = product["variants"][0]["offers"][0]["salePrice"] \
            if product["variants"][0]["offers"][0]["salePrice"] else product["variants"][0]["offers"][0]["price"]
        image_link = product["variants"][0]["offers"][0]["media"]["images"][0]
        products[name] = {
            "price": price,
            "image_link": image_link
        }

    return products

if __name__=="__main__":
    store = input('Loblaw or superstore? ')
    while store != 'loblaw' and store != 'superstore':
        store = input('Invalid input, try again: ')

    product = input('What item? ')

    products = make_pc_api_request(store, product)
    
    print(products)
