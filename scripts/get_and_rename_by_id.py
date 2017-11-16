from selenium import webdriver
from time import sleep
import yaml
import os
import shutil
import textract
import re
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

regex = '.*?(\\-(\\d+)\\))'
rg = re.compile(regex)
# download_pdf = 'C:\Users\Zach\Desktop\Classes\pdfs\download.pdf'
download_folder = 'C:\Users\Zach\Desktop\Classes\downloads\\'
pdf_folder = 'C:\Users\Zach\Desktop\Classes\pdfs\\' 

for i in range(46000, 99999, 1):    
	sleep(0.5)
	url = 'https://evaluations.scu.edu/?vclass=' + str(i) + '&vtrm=3820'
	# if os.path.exists(download_pdf)
	driver.get(url)

	for file in os.listdir(download_folder):
		shutil.move(download_folder + file, pdf_folder + file)
	# if driver.find_element_by_tag_name('aside') is not None:
		# print 'No PDF for ID: ' + str(i)
		# while not os.path.exists('C:\Users\Zach\Desktop\Classes\pdfs\download.pdf'):
			# sleep(0.1)
    
	# if os.path.exists(download_pdf):

		# Convert the pdf to a string
		# extracted_text = textract.process(download_pdf)
		
		# Search the extracted pdf file for the course id using the regex expression
		# match = rg.search(extracted_text)

		# Gets the second matched regex group (the course id number)
		# new_filename = match.group(2) + '.pdf'

		# print 'PDF for ID: ' + str(i) + ' downloaded as ' + new_filename

		# os.rename(download_pdf, 'C:\Users\Zach\Desktop\Classes\pdfs\\' + new_filename)		

		# os.remove(download_pdf)

driver.close()


