# selenium1.py

# CPLT52

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("quantum computing")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for results to load

    results = driver.find_elements(By.CSS_SELECTOR, "h3")
    print("Top Google results:")
    for r in results[:5]:
        print("-", r.text)
finally:
    driver.quit()
