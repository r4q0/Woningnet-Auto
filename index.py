from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

options = Options()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.1.2 Safari/602.3.12",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
]

random_user_agent = random.choice(user_agents)
options.set_preference("general.useragent.override", random_user_agent)

driver = webdriver.Firefox(options=options)

driver.get("https://www.studentenwoningweb.nl")

try:
    accept_cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cookiescript_accept"))
    )
    accept_cookies_button.click()
except Exception as e:
    print(f"Error clicking accept cookies button: {e}")

# Wait for the login form to be present
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "LoginForm"))
)

# Enter login credentials (replace with your actual credentials)


# Locate the username and password fields and enter the credentials
driver.find_element(By.ID, "Input_UsernameVal").send_keys(username)
driver.find_element(By.ID, "Input_PasswordVal").send_keys(password)

# Submit the login form
driver.find_element(By.ID, "b8-Button").click()

time.sleep(random.uniform(2,5))
# Now navigate to the target page
driver.get("https://www.studentenwoningweb.nl/WoningOverzicht")

# Wait for the expand button to be clickable
try: 
    expand_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@data-expression='' and contains(@class, 'font-bold') and text()='Match met je wensen']"))
    )
    expand_button.click()
except Exception as e:
    print(f"Error clicking expand button: {e}")

# Wait for the sort button to be clickable
try:
    sort_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@data-expression='' and text()='Tijd over om te reageren']"))
    )
    sort_button.click()
except Exception as e:
    print(f"Error clicking sort button: {e}")

# Find the parent div
parent_div = driver.find_element(By.XPATH, "//div[@data-list='' and contains(@class, 'list list-group border_width_line_top OSFillParent')]")
# Find all clickable divs inside the parent div
clickable_divs = parent_div.find_elements(By.CSS_SELECTOR, ".OSBlockWidget a")

# Open each div in a new tab
for i, div in enumerate(clickable_divs[:2]):
    href = div.get_attribute("href")
    driver.execute_script(f"window.open('{href}', '_blank');")
    time.sleep(random.uniform(1, 3))  # Random sleep to mimic human behavior

    print("opening new tab")
    driver.switch_to.window(driver.window_handles[-1])

    # Wait for the button to be clickable and click it
    try:
        reageren_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary OSFillParent' and text()='Reageren op deze Woning']"))
        )
        reageer_button_text = reageren_button.text  # Ensure we get the correct button
        print(f"Clicking button: {reageer_button_text} on tab {i + 1}")
        reageren_button.click()
    except Exception as e:
        print(f"Error clicking reageren button on tab {i + 1}: {e}")

    # After clicking, switch back to the main tab (index 0)
    time.sleep(random.uniform(1, 3))  # Random sleep before proceeding to the next div
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
driver.quit()