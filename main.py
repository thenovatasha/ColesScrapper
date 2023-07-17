from bs4 import BeautifulSoup
import requests
import csv
import time

def retrieve_data(html_text):

    html_text = html_text.text
    soup = BeautifulSoup(html_text, 'lxml')

    # filter out the products with no prices
    non_ads = soup.find_all('section', attrs={"data-testid":'product-tile'})

    # parse through all product tiles, retrieve info and store in lists
    product_names, product_prices, product_links, product_codes = [], [],[],[]
    for tile in non_ads:

        
        product_name = tile.find('h2', class_ = 'product__title').text.rstrip()
        try:
            product_price = tile.find('span', class_ = 'price__value').text
        except AttributeError:
            print(f'Check {product_name}, {page_num}')
            continue

        product_link ='coles.com.au' + tile.find('a', class_ = 'product__link').get("href")
        product_code = product_link.split('-')[-1]
        product_names.append(product_name)
        product_prices.append(product_price)
        product_links.append(product_link)
        product_codes.append(product_code)
        
    # Store data in csv
    data = list(zip(product_names, product_prices, product_codes, product_links))
    if len(data) == 0:
         return 0
    else: 
        return data
    

page_num = 1
data = []
while True:
    base_url = 'https://www.coles.com.au/on-special'
    URL = base_url + '?page=' + f'{page_num}'
    html_text = requests.get(URL)
    print(page_num)
    print(f'Response code is : {html_text.status_code}')
    data_found = retrieve_data(html_text)
    if html_text.status_code != 200 or data_found == 0:
        break
    data += data_found
    page_num += 1
    time.sleep(2)
    

with open('coles_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Product Name', 'Product Price', 'Product Code', 'Product Link'])
        writer.writerows(data)

print("Done successfully.")        