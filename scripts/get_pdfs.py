import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import yaml

def initialize():

	chromedriver = 'C:\Users\Zach\Desktop\Classes\chromedriver.exe'

	chrome_options = webdriver.ChromeOptions()
	# options.add_argument('--headless')
	# options.add_argument('--disable_gpu')
	# chrome_options.add_argument("--headless")
	# chrome_options.add_argument("--disable-gpu")

	browser = webdriver.Chrome(chromedriver, chrome_options=chrome_options)

	# Get scu.edu login info from YAML file
	conf = yaml.load(open('C:\Users\Zach\Desktop\Classes\config.yml'))
	username = conf['user']['username']
	password = conf['user']['password']

	browser.get('https://evaluations.scu.edu/')

	username_id = browser.find_element_by_id("username")
	password_id = browser.find_element_by_id("password")

	username_id.send_keys(username)
	password_id.send_keys(password)

	browser.find_element_by_name("_eventId_proceed").click()

	return browser

def main():
	browser = initialize()
	file = open("valid_ids.txt", "w")
	for i in range(10000, 99999, 1):
		try:
			url = 'https://evaluations.scu.edu/?vclass=' + str(i) + '&vtrm=3820'
			browser.get(url)
			download_icon = browser.find_element_by_tag_name('embed')
			file_address = download_icon.get_attribute('src')
			file.write(str(i) + '\n')
			print i
		except KeyboardInterrupt:
			exit()
		except:
			pass
	file.close()

if __name__ == "__main__":
	main()