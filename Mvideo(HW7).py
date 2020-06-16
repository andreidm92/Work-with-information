from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time
import json

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.mvideo.ru/")
time.sleep(6)
elem = driver.find_elements_by_xpath('//div[@class="gallery-layout"]')
actions = ActionChains(driver)
actions.move_to_element(elem[2])
actions.perform()
time.sleep(6)
while True:
    try:
        button = driver.find_element_by_xpath('//div[@class="gallery-layout"][2]//div[contains(@class, "sel-hits-block")]//a[@class = "next-btn sel-hits-button-next"]')
    except:
        break
    actions.move_to_element(button).click().perform()

client = MongoClient('localhost', 27017)
db = client['MVideoBase']
mvb = db.mvb

goods = driver.find_elements_by_xpath('//div[@class="gallery-layout"][2]//div[contains(@class, "sel-hits-block")]//li[@class="gallery-list-item height-ready"]//h4/a')
for good in goods:
    good = good.get_attribute('data-product-info')
    good = good.replace('\n', '')
    good = good.replace('\t', '')
    good = json.loads(good)
    mvb.insert_one(good)








