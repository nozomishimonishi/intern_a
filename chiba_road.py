# selenium.pyのコピー
from operator import index
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# chromedriverダウンロード
service = Service(executable_path=ChromeDriverManager().install())

# chromedriver読み込み
driver = webdriver.Chrome(service=service)
import os
import sys
from selenium.webdriver.chrome.options import Options
import time 
from selenium.webdriver.common.by import By
import chromedriver_binary
from selenium.webdriver.support.select import Select


def chiba_road(driver,ku,chou,banchi):
    # File Name
    FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_chiba_road/screen.png")

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
    select_1.select_by_visible_text(ku)  # 3番目のoptionタグを選択状態に
    time.sleep(2)

    dropdown_2 = driver.find_element(By.ID, "srh_search_drilldown_1_attrvalue_2")
    select_2 = Select(dropdown_2)
    select_2.select_by_visible_text(chou)

    time.sleep(2)

    if chou != "":
        dropdown_3 = driver.find_element(By.ID, "srh_search_drilldown_1_attrvalue_3")
        select_3 = Select(dropdown_3)
        chou = banchi
        select_3.select_by_visible_text(chou)
        time.sleep(2)

    element = driver.find_element(By.ID, 'srh_search_drilldown_1_btn').click()
    time.sleep(2)

    element = driver.find_element(By.ID, 'index_hidden').click()
    time.sleep(2)

    # get width and height of the page
    w = driver.execute_script("return document.body.scrollWidth;")
    h = driver.execute_script("return document.body.scrollHeight;")

    # set window size
    driver.set_window_size(w,h)
    time.sleep(2)

    element = driver.find_element(By.ID, 'sidemenu_tab_search').click()
    time.sleep(1)

    # Get Screen Shot
    driver.save_screenshot(FILENAME)
    time.sleep(1)
    
    # Close Web Browser
    driver.quit()


chiba_road(driver,"美浜区","磯辺２丁目","1")
