import csv
import os
from bs4 import BeautifulSoup
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from dotenv import load_dotenv
import time
load_dotenv()
options = Options()

# options.binary_location = '/opt/python/headless-chromium'
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--single-process')
# options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

account_sid = os.environ['account_sid']
auth_token = os.environ['token']
client = Client(account_sid, auth_token)

baseurl = r'https://us.vibram.com/shop/shop-all-products/mens-fivefingers-1/'
browser = webdriver.Chrome(
    executable_path=os.environ.get("driver_path"),
    options=options)
browser.get(baseurl)

time.sleep(2)
close_modal = browser.find_element_by_class_name("CloseButton__StyledSvgInput-sc-1mksxwr-0")
close_modal.click()

shoe_size = browser.find_element_by_id("swatch-44")
shoe_size.click()

time.sleep(2)

page_source = browser.page_source
soup = BeautifulSoup(page_source, 'html.parser')
product_selector = soup.find_all('div', class_='product-tile')
browser.quit()
for product in product_selector:
    price = product.find('span', class_='product-sales-price').get_text()
    name = product.find('a', class_='name-link')
    price_var = float(price[1:])
    name_var = name.get_text().strip().replace("\n", "").replace("\t", "")
    url_var = name['href']

    body = f"\n Product Name: {name_var} \n\n Price: ${price_var} \n\n Url: {url_var}"

    if price_var <= 90.0:
        message = client.messages.create(
            body=body,
            from_='+14087035615',
            to='+13055281278'
        )
        print(body)







