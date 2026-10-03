
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

url = "https://www.iqair.com/air-quality/sri-lanka/central/akurana/fect-akurana-outdoor"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get(url)

    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    print("Page title:", driver.title)
    print("Current URL:", driver.current_url)

    if "Security Checkpoint" in driver.title:
        print("Access blocked by security checkpoint.")
    else:
        print("Page loaded. Further content verification is needed.")

finally:
    driver.quit()


