from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def get_driver(headless=False):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    
    if headless:
        options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)