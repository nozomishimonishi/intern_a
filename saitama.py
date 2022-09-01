
from lib2to3.pgen2 import driver
import time
from turtle import towards
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
from selenium.webdriver.support.select import Select

import os
import sys
from selenium.webdriver.chrome.options import Options


# chromedriverダウンロード
service = Service(executable_path=ChromeDriverManager().install())
# chromedriver読み込み
driver = webdriver.Chrome(service=service)


# 住所から緯度経度を取り出す
import requests
import urllib

def saitama(zyusyo):

    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
    s_quote = urllib.parse.quote(zyusyo)
    response = requests.get(makeUrl + s_quote)
    response.json()[0]["geometry"]["coordinates"]
    ido = str(response.json()[0]["geometry"]["coordinates"][0])
    keido = str(response.json()[0]["geometry"]["coordinates"][1])

# 道路
    driver.get("https://www.sonicweb-asp.jp/saitama_g/map?theme=th_31#pos="+ido+","+keido)

    time.sleep(5)

    iframe = driver.find_element(By.XPATH,'//*[@id="agreement_mask"]')
    driver.switch_to.frame(iframe)
    driver.find_element(By.XPATH,'//*[@id="agree_btn_area"]/ul/li[1]/a').click()
    driver.switch_to.default_content()

    time.sleep(5)

    driver.save_screenshot('埼玉道路.png')

    time.sleep(3)

    driver.get("https://www.sonicweb-asp.jp/saitama_g/map?theme=th_90#pos="+ido+","+keido)

    time.sleep(5)

# 下水
    iframe = driver.find_element(By.XPATH,'//*[@id="agreement_mask"]')
    driver.switch_to.frame(iframe)
    driver.find_element(By.XPATH,'//*[@id="agree_btn_area"]/ul/li[1]/a').click()
    driver.switch_to.default_content()

    time.sleep(5)

    driver.save_screenshot('埼玉下水.png')

    time.sleep(3)

    driver.quit()

saitama("埼玉県さいたま市中央区新都心８")
