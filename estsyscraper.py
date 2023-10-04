from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv
import time
import json
import string

URL = "https://www.etsy.com/shop/ashjairocreations"

#image title price description

service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
#options.add_argument("--headless")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=service, options=options)
printable = set(string.printable)

driver.get(URL)
product_elements = driver.find_elements(By.CSS_SELECTOR, ".v2-listing-card")

product_data = []

product_links = []

# Extract links to each product
for product_element in product_elements:
    product_link = product_element.find_element(By.TAG_NAME, "a").get_attribute("href")
    product_links.append(product_link)

for link in product_links:
    driver.get(link)
    time.sleep(2)
    image_link = []
    title = driver.find_element(By.CSS_SELECTOR, "h1.wt-text-body-01").text
    price = driver.find_element(By.CSS_SELECTOR, ".wt-text-title-largest").text
    desc = driver.find_element(By.CSS_SELECTOR, "p.wt-text-body-01").text
    images = driver.find_elements(By.CSS_SELECTOR, ".listing-page-image-carousel-component .carousel-image")
    for image in images:
        image_link.append(image.get_attribute("src"))
    print(title)
    print(price)
    print(desc)
    time.sleep(4)