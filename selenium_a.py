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

def chiba_gesui(driver,ku,chou,chome,banchi):
    FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_chiba_gesui/screen.png")

    driver.get("http://s-page.tumsy.com/chibagesui/index.html")
    
    time.sleep(2)
    
    iframe = driver.find_element(By.XPATH,'/html/frameset/frame')
    driver.switch_to.frame(iframe)
    driver.find_element(By.XPATH,'//*[@id="LinkButton1"]').click()
    driver.switch_to.default_content()
    
    time.sleep(5)
    
    iframe = driver.find_element(By.XPATH,'/html/frameset/frame')
    driver.switch_to.frame(iframe)
    
    dropdown_1 = driver.find_element(By.ID,"ELM_CMB_LEV1")
    select_1 = Select(dropdown_1)
    select_1.select_by_visible_text(ku)
    
    time.sleep(2)
    
    dropdown_2 = driver.find_element(By.ID,"ELM_CMB_LEV2")
    select_2 = Select(dropdown_2)
    select_2.select_by_visible_text(chou)
    
    time.sleep(2)
    if chome != " ":
        dropdown_3 = driver.find_element(By.ID,"ELM_CMB_LEV3")
        select_3 = Select(dropdown_3)
        select_3.select_by_visible_text(chome)
        
    time.sleep(2)
    
    dropdown_4 = driver.find_element(By.ID,"ELM_CMB_LEV4")
    select_4 = Select(dropdown_4)
    select_4.select_by_visible_text(banchi)
    
    time.sleep(2)
    
    driver.find_element(By.XPATH,'//*[@id="btnAddSchDlgOK"]').click()
    driver.switch_to.default_content()
    
    time.sleep(5)
    
    driver.save_screenshot('FALENAME.png')
    
    time.sleep(3)

    driver.quit()
    
    
    
chiba_gesui(driver,"中央区","今井","１丁目","１番")