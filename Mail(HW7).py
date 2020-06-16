from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pymongo import MongoClient

driver = webdriver.Chrome()
driver.get('https://account.mail.ru/login')
time.sleep(2)
elem = driver.find_element_by_class_name('c0163')
time.sleep(5)
elem.send_keys('study.ai_172')
elem.send_keys(Keys.RETURN)
elem = driver.find_element_by_xpath('//input[@name="password"]')
elem.send_keys('NextPassword172')
elem.send_keys(Keys.RETURN)
time.sleep(5)
#assert "Входящие - Почта Mail.ru" in driver.title
profile = driver.find_element_by_xpath('//a[@class="llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal"][1]')
driver.get(profile.get_attribute('href'))
time.sleep(10)

client = MongoClient('localhost', 27017)
db = client['MailBase']
mb = db.mb

while True:
    mails_data = {}
    mails_data['Sender'] = driver.find_element_by_class_name("letter__author").text
    mails_data['Time'] = driver.find_element_by_class_name("letter__date").text
    mails_data['Theme'] = driver.find_element_by_class_name("thread__subject-line").text
    mails_data['Text'] = driver.find_element_by_class_name("letter-body").text
    mb.insert_one(mails_data)
    profile = driver.find_element_by_class_name("button2_arrow-down")
    if profile.is_enabled() != True:
        break
    profile.click()
    time.sleep(2)



