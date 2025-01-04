from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Setup Firefox options
options = Options()

# Set a real User-Agent string (replace with a valid one)
options.set_preference("general.useragent.override", "Your-User-Agent-String-Here")  

# Initialize the browser
driver = webdriver.Firefox(options=options)

# Navigate to the target website (initial request to set the cookies)
driver.get("https://amsterdam.mijndak.nl/")

# Load cookies from the file
cookies = []
with open("cookies.txt", "r") as file:
    for line in file:
        if not line.startswith("#") and line.strip():
            parts = line.strip().split("\t")
            if len(parts) == 7:
                cookie = {
                    "domain": parts[0],
                    "path": parts[2],
                    "secure": parts[3].upper() == "TRUE",
                    "expiry": int(parts[4]),
                    "name": parts[5],
                    "value": parts[6]
                }
                cookies.append(cookie)

# Add cookies to the browser after navigating to the target website
for cookie in cookies:
    driver.add_cookie(cookie)

# Introducing random sleep delays between actions to mimic human behavior
time.sleep(random.uniform(2, 5))  # Wait between 2 to 5 seconds

# Now navigate to the target page after setting cookies
driver.get("https://amsterdam.mijndak.nl/WoningOverzicht")


# Wait for the expand button to be clickable
expand_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[@data-expression='' and contains(@class, 'font-bold') and text()='Match met je wensen']"))
)


# Click the button to expand the options
expand_button.click()


sort_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[@data-expression='' and text()='Tijd over om te reageren']"))
)


sort_button.click()

