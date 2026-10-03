from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    url = "https://www.iqair.com/air-quality/sri-lanka/central/akurana/fect-akurana-outdoor"
    driver.get(url)

    print("Page title:", driver.title)
    print("Successfully opened IQAir page.")

finally:
    driver.quit()

