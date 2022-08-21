from selenium import webdriver

# Chromedriver location
driver_location = "/usr/bin/chromedriver"

# Google Chrome location
binary_location = "/usr/bin/google-chrome"

option = webdriver.ChromeOptions()
option.binary_location = binary_location

driver = webdriver.Chrome()

driver.get("https://uitspraken.rechtspraak.nl/InzienDocument?id=ECLI:NL:RBLIM:2022:3355")

element = driver.find_element("content")

print(element)