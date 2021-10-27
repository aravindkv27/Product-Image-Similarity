from selenium import webdriver
import os
import time
import urllib.request
from selenium.webdriver.common.keys import Keys
import pandas as pd

PATH="/home/aravind/Featurepreneur/chromedriver"

driver=webdriver.Chrome(PATH)

driver.get('https://www.amazon.in/')

search=driver.find_element_by_id("twotabsearchtextbox")

search.send_keys("Mobiles")

search.send_keys(Keys.RETURN)

total_images=[]

mobiles=driver.find_elements_by_xpath("//*[@class='s-image']")

for img in mobiles:
    mobiles.get_attribute('src')
    total_images.append(img)


# df = pd.read_csv('product_images.csv')
product_image=pd.DataFrame(total_images)

product_image.to_csv('product_images.csv')