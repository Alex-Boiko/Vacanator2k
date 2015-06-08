__author__ = 'AnubiS'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import date
from dateutil.parser import parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


FROM = "Munich"
TO = ["Katmandu", "Lima"]
TODAY = date.today()
depature_date = parse('2015-09-20')
return_date = parse('2015-10-05')


def find_flight(from_city, to_city, depature_date, arrival_date):
    # FROM
    driver = webdriver.Firefox()
    driver.get("http://www.skyscanner.pl")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "js-origin-input")))
    except TimeoutException:
        print "Can't reach skyscanner page"
        driver.close()
    # raise TimeoutException(message)
    #     selenium.common.exceptions.TimeoutException: Message: "Can't reach skyscanner page":
    #
    #driver.quit()
    origin = driver.find_element_by_id("js-origin-input")
    actions = ActionChains(driver)
    actions.double_click(origin)
    actions.perform()
    origin.send_keys(from_city)
    time.sleep(1)
    origin.send_keys(Keys.RETURN)

    #TO
    destination = driver.find_element_by_id("js-destination-input")
    actions.double_click(destination)
    actions.perform()
    destination.send_keys(to_city)
    time.sleep(1)
    destination.send_keys(Keys.RETURN)
    destination.send_keys(Keys.RETURN)

    #SELECTING DATES
    date_selector(driver, depature_date, return_date)
    #MAKING SEARCH
    searchButton = driver.find_element_by_id("js-search-button")
    searchButton.click()
    time.sleep(10)   #Remove implicit wait and use explicit one as example below
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "day-progress-meter clearfix hidden")))
    price_elements = driver.find_elements_by_class_name("filter-sub")
    str_prices = []
    clear_prices = []
    prices = []
    for obj in price_elements:
        str_prices.append(obj.text)
        clear_prices = [p for p in str_prices if p != 'brak']   # Filtering out 'none' price values
    print clear_prices
    for clear_price in clear_prices:
        #Let's remove letters and convert price to integer. Example: "1 234 zl" -> 1234
        prices.append(int(''.join(str(elem) for elem in [str(s) for s in clear_price.split() if s.isdigit()])))
    sorted_prices = sorted(list(set(prices)))
    return to_city, sorted_prices


def date_selector(driver, depature_date, return_date):
        #Depature date-------------------------------------------------------------------------------------------------
        month_till_depature_date = abs((TODAY.year - depature_date.year)*12 + TODAY.month - depature_date.month)
        depature_date_elem = driver.find_element_by_id("js-depart-input")
        #driver.execute_script("document.getElementById('js-depart-input').value = '2015-06-01';")
        depature_date_elem.click()
        time.sleep(1)
        if month_till_depature_date > 0:
            #print month_till_depature_date
            for x in range(0, month_till_depature_date):
                one_month_further_elem = driver.find_element_by_class_name("next")
                one_month_further_elem.click()
                time.sleep(0.5)
            driver.find_element_by_link_text(str(depature_date.day)).click()
            time.sleep(0.5)
        else:
            driver.find_element_by_link_text(str(depature_date.day)).click()
        #Return date---------------------------------------------------------------------------------------------------
        month_till_return_date = abs((TODAY.year - return_date.year)*12 + TODAY.month - return_date.month)
        return_date_elem = driver.find_element_by_id("js-return-input")
        return_date_elem.click()
        time.sleep(1)
        if month_till_return_date > 0:
            for x in range(0, month_till_return_date):
                one_month_further_elem = driver.find_elements_by_class_name("next")
                one_month_further_elem[1].click()
                time.sleep(0.5)
            driver.find_element_by_partial_link_text(str(return_date.day)).click()
        else:
            driver.find_element_by_link_text(str(return_date.day)).click()
        #one_month_further_elem = driver.find_element_by_class_name("next")
        #driver.execute_script("document.getElementById('js-return-input').value = '2015-07-01';")

# def results_aggrigator():
prices = []
for city in TO:
    prices.append(find_flight(FROM, city, depature_date, return_date))
print prices