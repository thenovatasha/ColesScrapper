from bs4 import BeautifulSoup
import requests
import csv
import time

# Parse through each category links and category names and store in a list
category_links = []
main_url = 'https://www.coles.com.au/browse'
main_html = requests.get(main_url).text
soup_categories = BeautifulSoup(main_html, "lxml")
category_tiles = soup_categories.find("ul", class_="sc-fc107670-0")

for tile in category_tiles:
     category_link = tile.find("a", attrs={'data-testid': 'category-card'}).get('href')
     category_name = tile.find("a", attrs={'data-testid': 'category-card'}).get('aria-label')


     category_links.append((category_link, category_name))

def retrieve_data(html, category_name):

    html_text = html.text
    soup = BeautifulSoup(html_text, 'lxml')

    # filter out the products with no prices
    non_ads = soup.find_all('section', attrs={"data-testid":'product-tile'})

    # parse through all product tiles, retrieve info and store in lists
    product_names, product_prices, product_links, product_codes, category_names = [], [], [], [], []
    for tile in non_ads:

        product_name = tile.find('h2', class_ = 'product__title').text.rstrip()
        # check and add tiles which do not have a price or are out of stock
        try:
            product_price = tile.find('span', class_ = 'price__value').text
        except AttributeError:
            print(f'Check {product_name}, {page_num}')
            product_names.append(product_name)
            product_prices.append('Out of Stock')
            product_links.append('Out of Stock')
            product_codes.append('Out of Stock')
            category_names.append(category_name)
            continue

        product_link ='coles.com.au' + tile.find('a', class_ = 'product__link').get("href")
        product_code = product_link.split('-')[-1]
        product_names.append(product_name)
        product_prices.append(product_price)
        product_links.append(product_link)
        product_codes.append(product_code)
        category_names.append(category_name)
        
    # Store data in csv
    data = list(zip(product_names, product_prices, product_codes, product_links, category_names))
    if len(data) == 0:
         return 0
    else: 
        return data
    
data = []
BASE_URL = 'https://www.coles.com.au'
for category_link, category_name in category_links:
    page_num = 1
    while True:
        
        URL = BASE_URL + category_link + '?page=' + f'{page_num}'
        html = requests.get(URL)
        # track progress and debug
        print(f'Currently scraping {page_num}, from {category_name}')
        print(f'Response code is : {html.status_code}')
        data_found = retrieve_data(html, category_name)
        # Send to sleep for 2 minutes to prevent access denial.
        if html.status_code == 403:
            time.sleep(120)
        if html.status_code != 200 or data_found == 0:
            break
        
        data += data_found
        page_num += 1
        time.sleep(2)
    
# write data as a csv format
with open('coles_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Product Name', 'Product Price', 'Product Code', 'Product Link', 'Category'])
        writer.writerows(data)

print("Done successfully.")

# to do:
# 1. refactor code into more reusable functions
# 2. add more error handling
# 3. add more comments
# 4. add more data to be scraped (e.g. product description, product image, etc.)