
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json
import datetime

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

data = [
	{
		'state': 'California',
		'city': 'Half Moon Bay'
	},
	{
		'state': 'California',
		'city': 'Huntington Beach'
	},
	{
		'state': 'Rhode Island',
		'city': 'Providence'
	},
	{
		'state': 'North Carolina',
		'city': 'Wrightsville Beach'
	}
]

return_data = []

for datum in data:
	driver.get("https://www.tide-forecast.com/")

	driver.implicitly_wait(2)

	state_select = Select(driver.find_element(By.XPATH, '//*[@id="region_id"]'))
	state_select.select_by_visible_text(datum['state'])
	driver.implicitly_wait(1)

	city_select = Select(driver.find_element(By.XPATH, '//*[@id="location_filename_part"]'))
	city_select.select_by_visible_text(datum['city'])

	#wait for table data to load
	#in this scneario I am waiting 5 seconds, you can do a wait until the table data shows up as well
	driver.implicitly_wait(5)

	# we know in this problem that the sunrise and sunset will always be table elements 2 and 4 respectively
	# we could do it dynamically, but we only have an hour
	sunrise = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[1]/div[1]/div[3]/div[2]/div/div/table/tbody/tr[6]/td[2]/div')
	sunrise = datetime.datetime.strptime(sunrise.text, "%I:%M%p")
	sunset = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[1]/div[1]/div[3]/div[2]/div/div/table/tbody/tr[6]/td[4]/div')
	sunset = datetime.datetime.strptime(sunset.text, "%I:%M%p")

	tides = driver.find_elements(By.XPATH, '/html/body/main/div[3]/div[1]/section[1]/div/div[1]/div[1]/table/tbody/tr')
	for tide in tides:
		if "Low Tide" in tide.text:
			tide_time = tide.find_element(By.XPATH, './/b')
			tide_date = tide.find_element(By.XPATH, './/span')
			tide_height = tide.find_element(By.XPATH, '//b[@class="js-two-units-length-value__primary"]')
			tide_time_converted = datetime.datetime.strptime(tide_time.text, "%I:%M %p")
			if sunrise < tide_time_converted and sunset > tide_time_converted:
				print('Low tide found between sunrise and sunset')
				return_data.append({'time': tide_time.text, 'date': tide_date.text, 'height': tide_height.text})

	#just sleeping here so there is an obvious differential
	time.sleep(3)

print(return_data)
driver.quit()