from unicodedata import name

from lib2to3.pgen2 import driver
import time
from turtle import towards
from h11 import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
from selenium.webdriver.support.select import Select

from selenium.webdriver.chrome.options import Options

from operator import index

import requests
import urllib
from platform import machine


def saitama(zyusyo): #埼玉の住所を入力しスクショを２枚とる
    can_saitama = True

    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
    s_quote = urllib.parse.quote(zyusyo)
    response = requests.get(makeUrl + s_quote)
    response.json()[0]["geometry"]["coordinates"]
    ido = str(response.json()[0]["geometry"]["coordinates"][0])
    keido = str(response.json()[0]["geometry"]["coordinates"][1])

    if (response.json()[0]["geometry"]["coordinates"]) != None:
        if "さいたま市" in zyusyo:

            # chromedriverダウンロード
            service = Service(executable_path=ChromeDriverManager().install())
            # chromedriver読み込み
            driver = webdriver.Chrome(service=service)

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
        else:
            #print("エリア外")
            can_saitama = False
            exit()
    else:
        #print('存在しない住所')
        can_saitama = False
        exit()
    
    driver.quit()
    return can_saitama