from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Setup Firefox options
options = Options()
driver = webdriver.Firefox(options=options)

# Load cookies from the file (you should have exported these earlier)
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

# Open the target website
driver.get("https://amsterdam.mijndak.nl/WoningOverzicht")

# Add cookies to the browser
for cookie in cookies:
    driver.add_cookie(cookie)

# After adding cookies, refresh to use them
driver.refresh()

# Now you are logged in with the session data
driver.get("https://amsterdam.mijndak.nl/WoningOverzicht")
