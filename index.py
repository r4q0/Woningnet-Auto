import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import schedule
from dotenv import load_dotenv
import random
import os

# Configure logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
def run_script():
    load_dotenv()

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

    try:
        driver.get(os.getenv('URL'))

        try:
            accept_cookies_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "cookiescript_accept"))
            )
            accept_cookies_button.click()
        except Exception as e:
            message = f"Error clicking accept cookies button: {e}"
            print(message)
            logging.info(message)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "LoginForm"))
        )

        username = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')

        driver.find_element(By.ID, "Input_UsernameVal").send_keys(username)
        driver.find_element(By.ID, "Input_PasswordVal").send_keys(password)

        driver.find_element(By.ID, "b8-Button").click()

        time.sleep(random.uniform(2, 5))
        driver.get(os.getenv('URL') + "/WoningOverzicht")

        try: 
            expand_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-expression='' and contains(@class, 'font-bold') and text()='Match met je wensen']"))
            )
            expand_button.click()
        except Exception as e:
            message = f"Error clicking expand button: {e}"
            print(message)
            logging.info(message)

        try:
            sort_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-expression='' and text()='Tijd over om te reageren']"))
            )
            sort_button.click()
        except Exception as e:
            message = f"Error clicking sort button: {e}"
            print(message)
            logging.info(message)

        parent_div = driver.find_element(By.XPATH, "//div[@data-list='' and contains(@class, 'list list-group border_width_line_top OSFillParent')]")
        clickable_divs = parent_div.find_elements(By.CSS_SELECTOR, ".OSBlockWidget a")

        for i, div in enumerate(clickable_divs[:int(os.getenv('MAX-INSCHRIJVINGEN'))]):
            href = div.get_attribute("href")
            driver.execute_script(f"window.open('{href}', '_blank');")
            time.sleep(random.uniform(1, 3))

            message = f"opening new tab"
            print(message)
            logging.info(message)
            driver.switch_to.window(driver.window_handles[-1])

            try:
                reageren_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary OSFillParent' and text()='Reageren op deze Woning']"))
                )
                reageer_button_text = reageren_button.text
                message = f"Clicking button: {reageer_button_text} on tab {i + 1}"
                print(message)
                logging.info(message)
                reageren_button.click()
            except Exception as e:
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-secondary OSFillParent' and text()='Reactie intrekken']"))
                    )
                    message = f"Already Reacted to this listing on tab {i + 1}"
                    print(message)
                    logging.info(message)
                except Exception as inner_e:
                    message = f"Error clicking reageren button on tab {i + 1}: {e}"
                    print(message)
                    logging.info(message)

            time.sleep(random.uniform(1, 3))
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        
        message = f"Succesvol {os.getenv('MAX-INSCHRIJVINGEN')} keer ingeschreven op {os.getenv('URL')}"
        print(message)
        logging.info(message)
        
    except Exception as e:
        message = f"Check je .env variabelen: {e}"
        print(message)
        logging.info(message)
    finally:
        driver.quit()


schedule.every().monday.do(run_script)
schedule.every().friday.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(60)
