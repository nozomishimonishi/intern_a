import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time 

from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
driver = webdriver.Chrome()

# File Name
FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image/screen.png")

driver.get("https://www.google.co.jp/maps/@33.5001886,137.1538646,5z?hl=ja")

element = driver.find_element(By.ID, 'searchboxinput').send_keys('GINZA SIX')

element = driver.find_element(By.ID, 'searchbox-searchbutton').click()


# get width and height of the page
w = driver.execute_script("return document.body.scrollWidth;")
h = driver.execute_script("return document.body.scrollHeight;")

# set window size
driver.set_window_size(w,h)

time.sleep(10)


# Get Screen Shot
driver.save_screenshot(FILENAME)



time.sleep(30)
