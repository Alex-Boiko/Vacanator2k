__author__ = 'AnubiS'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Firefox()
driver.get("http://www.skyscanner.com")
origin = driver.find_element_by_id("js-origin-input")
actions = ActionChains(driver)
actions.double_click(origin)
actions.perform()
origin.send_keys("Munich")
time.sleep(3)
origin.send_keys(Keys.RETURN)
destination = driver.find_element_by_id("js-destination-input")
destination.send_keys("Katmandu")
time.sleep(3)
destination.send_keys(Keys.RETURN)
destination.send_keys(Keys.RETURN)
searchButton = driver.find_element_by_id("js-search-button")
searchButton.click()
#blabla
#assert "No results found." not in driver.page_source
time.sleep(15)
driver.close()