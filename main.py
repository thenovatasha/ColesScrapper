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
    
# get categories links
main_url = 'https://www.coles.com.au/browse'
main_html = requests.get(main_url).text
soup_categories = BeautifulSoup(main_html, "lxml")
category_tiles = soup_categories.find("ul", class_="sc-fc107670-0")

category_links = []
for tile in category_tiles:
     category_link = tile.find("a", attrs={'data-testid': 'category-card'}).get('href')
     category_links.append(category_link)


data = []
BASE_URL = 'https://www.coles.com.au'
for category in category_links:
    page_num = 1
    while True:
        
        URL = BASE_URL + category + '?page=' + f'{page_num}'
        html_text = requests.get(URL)
        print(page_num)
        print(category)
        print(f'Response code is : {html_text.status_code}')
        data_found = retrieve_data(html_text)
        if html_text.status_code != 200 or data_found == 0:
            break
        data += data_found
        page_num += 1
        time.sleep(2)
    

with open('coles_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Product Name', 'Product Price', 'Product Code', 'Product Link', 'Category'])
        writer.writerows(data)

print("Done successfully.")