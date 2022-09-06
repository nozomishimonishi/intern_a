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


def chiba_gesui(ku,machi,chome,banchi): #千葉住所を入力して下水をスクショする
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    #FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_chiba_gesui/screen.png")

    can_gesui = True

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
    try:
        select_1.select_by_visible_text(ku)
    except NoSuchElementException:
        can_gesui = False
        driver.quit()
        return can_gesui

    
    time.sleep(2)
    
    dropdown_2 = driver.find_element(By.ID,"ELM_CMB_LEV2")
    select_2 = Select(dropdown_2)
    try:
        select_2.select_by_visible_text(machi)
    except NoSuchElementException:
        can_gesui = False
        driver.quit()
        return can_gesui
    
    time.sleep(2)

    dropdown_3 = driver.find_element(By.ID,"ELM_CMB_LEV3")
    select_3 = Select(dropdown_3)
    try:
        select_3.select_by_visible_text(chome)
    except NoSuchElementException:
        can_gesui = False
        driver.quit()
        return can_gesui
    time.sleep(2)
    
    dropdown_4 = driver.find_element(By.ID,"ELM_CMB_LEV4")
    select_4 = Select(dropdown_4)
    # all_options_4 = select_4.options
    # for option_4 in all_options_4:
    #     print(option_4.text)
    try:
        select_4.select_by_visible_text(banchi)
    except NoSuchElementException:
        can_gesui = False
        driver.quit()
        return can_gesui
    
    time.sleep(2)
    
    driver.find_element(By.XPATH,'//*[@id="btnAddSchDlgOK"]').click()
    driver.switch_to.default_content()
    
    time.sleep(5)
    
    driver.save_screenshot('千葉下水.png')
    
    time.sleep(3)
    driver.quit()
    return can_gesui