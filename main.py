from bs4 import BeautifulSoup
import requests

URL = 'https://www.coles.com.au/on-special'
# go through all the pages. 
# Find all products in url
html_text = requests.get(URL).text
soup = BeautifulSoup(html_text, 'lxml')

# except the ones with no prices
non_ads = soup.find_all('section', attrs={"data-testid":'product-tile'})

# parse through all tiles and store in zip
all_names, all_prices = [], []
for tile in non_ads:

    product_price = tile.find('span', class_ = 'price__value').text
    product_name = tile.find('h2', class_ = 'product__title').text.rstrip()
    all_names.append(product_name)
    all_prices.append(product_price)
    # for each product, get the link from the a tag.
        # enter the link and get the product id.

data = zip(all_names, all_prices)
print(list(data))



