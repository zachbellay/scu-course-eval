from selenium import webdriver
from time import sleep
import yaml
import os
import shutil
from selenium.common.exceptions import NoSuchElementException
from time import sleep

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
download_folder = "C:\Users\Zach\Desktop\Classes\pdfs"    
chromedriver = 'C:\Users\Zach\Desktop\Classes\chromedriver.exe'

profile = {"plugins.plugins_list": [{"enabled": False,
"name": "Chrome PDF Viewer"}],
"download.default_directory": download_folder,
"download.extensions_to_open": ""}

options.add_experimental_option("prefs", profile)

driver = webdriver.Chrome(chromedriver, chrome_options = options)

conf = yaml.load(open('C:\Users\Zach\Desktop\Classes\config.yml'))
username = conf['user']['username']
password = conf['user']['password']

driver.get('https://evaluations.scu.edu/')

username_id = driver.find_element_by_id("username")
password_id = driver.find_element_by_id("password")

username_id.send_keys(username)
password_id.send_keys(password)

driver.find_element_by_name("_eventId_proceed").click()


for i in range(46000, 99999, 1):    
    sleep(0.5)
    url = 'https://evaluations.scu.edu/?vclass=' + str(i) + '&vtrm=3820'
    driver.get(url)

driver.close()
