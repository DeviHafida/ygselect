import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

@pytest.fixture(scope="function")
def driver():
    """Fixture untuk menyediakan WebDriver dengan driver manual"""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    
    # Path ke chromedriver manual (sama seperti test_manual.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(current_dir, "drivers", "chromedriver.exe")
    
    # Cek apakah file ada
    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"chromedriver.exe tidak ditemukan di {driver_path}")
    
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(120)
    
    yield driver
    
    driver.quit()

@pytest.fixture
def base_url():
    return "https://en.ygselect.com/index.html"