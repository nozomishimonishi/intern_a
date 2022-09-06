from unicodedata import name

from lib2to3.pgen2 import driver
import time
from turtle import towards
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
from selenium.webdriver.support.select import Select

import sys
from selenium.webdriver.chrome.options import Options

from operator import index
from selenium.common.exceptions import NoSuchElementException

def chiba_road(ku,machi,banchi): #千葉の住所を入力して道路をスクショ
    # TypeError
    can_road = True

    # chromedriverダウンロード
    service = Service(executable_path=ChromeDriverManager().install())
    # chromedriver読み込み
    driver = webdriver.Chrome(service=service)

    # File Name
    #FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_chiba_road/screen.png")

    driver.get("https://webgis.alandis.jp/chiba12/portal/nintei.html")
    time.sleep(2)

    driver.get("https://webgis.alandis.jp/chiba12/webgis/index.php/autologin_jswebgis?ap=jsWebGIS&m=2&u=guest1&x=15595700.6909091&y=4256412.71232589&s=5000&rs=3857&li=1&si=0")
    time.sleep(10)

    element = driver.find_element(By.ID, 'sidemenu_tab_search').click()
    time.sleep(1)

    element = driver.find_element(By.ID, 'sidemenu_menu_search_drilldown_1').click()
    time.sleep(3)

    dropdown_1 = driver.find_element(By.ID, 'srh_search_drilldown_1_attrvalue_1')
    select_1 = Select(dropdown_1)
    try:
        select_1.select_by_visible_text(ku)  # 3番目のoptionタグを選択状態に
    except NoSuchElementException:
        driver.quit()
        can_road = False
        return can_road
    time.sleep(2)

    dropdown_2 = driver.find_element(By.ID, "srh_search_drilldown_1_attrvalue_2")
    select_2 = Select(dropdown_2)
    # all_options_2 = select_2.options
    # for option_2 in all_options_2:
    #     print(option_2.text)
    try:
        select_2.select_by_visible_text(machi)
    except NoSuchElementException:
        driver.quit()
        can_road = False
        return can_road

    time.sleep(2)

    
    dropdown_3 = driver.find_element(By.ID, "srh_search_drilldown_1_attrvalue_3")
    select_3 = Select(dropdown_3)
    # all_options_3 = select_3.options
    # for option_3 in all_options_3:
    #     print(option_3.text)
    try:
        select_3.select_by_visible_text(banchi)
    except NoSuchElementException:
        can_road = False
        # Close Web Browser
        driver.quit()
        return can_road
    time.sleep(2)

    element = driver.find_element(By.ID, 'srh_search_drilldown_1_btn').click()
    time.sleep(2)

    element = driver.find_element(By.ID, 'index_hidden').click()

    time.sleep(2)

    element = driver.find_element(By.ID, 'sidemenu_tab_search').click()
    time.sleep(1)

    # Get Screen Shot
    driver.save_screenshot('千葉道路.png')
    time.sleep(1)
    
    # Close Web Browser
    driver.quit()
    return can_road