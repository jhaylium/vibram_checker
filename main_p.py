from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from twilio.rest import Client
from random import randrange
from dotenv import load_dotenv
import os

load_dotenv()


account_sid = os.environ['account_sid']
auth_token = os.environ['token']
client = Client(account_sid, auth_token)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # url_size_44 = r'https://us.vibram.com/shop/shop-all-products/mens-fivefingers-1/#prefn1=size&prefv1=44'
        url_size_44 = r'https://us.googleoop.com/'
        page.goto(url_size_44)
        soup = BeautifulSoup(page.inner_html('[id="main"]'), 'html.parser')
        product_selector = soup.find_all('div', class_='product-tile')
        products = []
        for product in product_selector:
            price = product.find('span', class_='product-sales-price').get_text()
            name = product.find('a', class_='name-link')
            price_var = float(price[1:])
            name_var = name.get_text().strip().replace("\n", "").replace("\t", "")
            url_var = name['href']
            shoe_data = [name_var, price_var, url_var]
            body = f"\n Product Name: {name_var} \n\n Price: ${price_var} \n\n Url: {url_var}"
            if price_var < 90.0:
                message = client.messages.create(
                    body=body,
                    from_=os.environ['from_number'],
                    to=os.environ['to_number']
                )

            print(body)
        browser.close()
except Exception as err:
    body = str(err)[:1559]
    message = client.messages.create(
        body=err,
        from_=os.environ['from_number'],
        to=os.environ['to_number']
    )

def get_user_agent(num):
    agent = {
        '1':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
        '2':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        '3':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.35',
        '4': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
        '5': 'Mozilla/5.0 (Linux; Android12; Pixel3XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.58 Safari/537.36',
    }
    return agent[num]

# ua_num = str(randrange(1, 5, 1))
# header = {
#     'User-Agent': get_user_agent(ua_num),
#     'Accept-Encoding': 'identity'
# }
# print(header)
# base_url = r'https://us.vibram.com/shop/shop-all-products/mens-fivefingers-1/'
# url_size_44 = r'https://us.vibram.com/shop/shop-all-products/mens-fivefingers-1/#prefn1=size&prefv1=44'

# r = requests.get(url_size_44, headers=header)
# soup = BeautifulSoup(r.content, 'html.parser')
# soup = BeautifulSoup(r.content, 'html.parser')
# product_selector = soup.find_all('div', class_='product-tile')
# for product in product_selector:
#     price = product.find('span', class_='product-sales-price').get_text()
#     name = product.find('a', class_='name-link')
#     price_var = float(price[1:])
#     name_var = name.get_text().strip().replace("\n", "").replace("\t", "")
#     url_var = name['href']
#
#     body = f"\n Product Name: {name_var} \n\n Price: ${price_var} \n\n Url: {url_var}"
#
#     print(body)




