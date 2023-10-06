from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import time
import string
import os
import re

#Replace this url with an Etsy website you want to scrape
#Make sure its the home page of a store, eg: https://www.etsy.com/shop/ashjairocreations
URL = "https://www.odeonboutique.com/collections/tops?page=2"

ROOTDIR = "./ShopifyData"
try:
    os.mkdir(ROOTDIR)
except:
    print("rootdir exists :DD")

service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--headless")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=service, options=options)
printable = set(string.printable)

driver.get(URL)
product_elements = driver.find_elements(By.CSS_SELECTOR, ".grid--no-gutters .product-card ")

product_data = []
product_links = []

# Extract links to each product
for product_element in product_elements:
    product_link = product_element.get_attribute("href")
    product_links.append(product_link)
print(len(product_links))

for link in product_links:
    driver.get(link)
    time.sleep(2)
    
    try:
        image_link = []
        title = driver.find_element(By.CSS_SELECTOR, ".product-single__title").text
        price = driver.find_element(By.CSS_SELECTOR, ".product-single__price").text
        desc = ""
        try:
            desc = driver.find_element(By.CSS_SELECTOR, ".rte p").text
        except:
            desc = ""
        images = driver.find_elements(By.CSS_SELECTOR, ".js-modal-open-product-modal")
        for image in images:
            image_link.append(image.get_attribute("href"))
        path_title = re.sub(r'[^\w_. -]', '_', title)
        mydir = ROOTDIR + "/" + path_title
        try: 
            os.mkdir(mydir)
        except:
            pass
        file1 = open(mydir + "/info.txt","w")
        file1.write(title + "\n")
        file1.write(price + "\n")
        file1.write(desc)
        file1.close()

        for i in range(len(image_link)):
            data = requests.get(image_link[i]).content
            index = i-1
            if index == -1:
                index = ""
            f = open(mydir + "/image" + str(index) + ".jpg", 'wb')
            f.write(data)
            f.close()
        time.sleep(.5)
    except:
        print("oopsie poopsie")