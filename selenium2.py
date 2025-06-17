# selenium1.py

# CPLT66

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_options = Options()
# chrome_options.add_argument("--headless=new")  # Use new headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
service = Service("/usr/bin/chromedriver")  # Path to chromedriver in WSL2
driver = webdriver.Chrome(service=service, options=chrome_options)
try:
    driver.get("https://duckduckgo.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("quantum computing")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Wait longer for results to load

    results = driver.find_elements(By.CSS_SELECTOR, "h2 a.result__a")
    print("Top DuckDuckGo results:")
    for r in results[:5]:
        print("-", r.text)

    # Debug: print the first 500 characters of the page source
    print("\n[DEBUG] Page source snippet:")
    print(driver.page_source[:500])

    # Keep browser open for 30 seconds for inspection
    print("\n[INFO] Browser will remain open for 30 seconds...")
    time.sleep(30)
finally:
    driver.quit()
