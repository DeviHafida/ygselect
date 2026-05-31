from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

driver.set_page_load_timeout(120)

driver.get("https://en.ygselect.com/index.html")

print(driver.title)

time.sleep(10)

driver.quit()