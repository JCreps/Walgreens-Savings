import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Constants
CHROME_DRIVER_PATH = r"" #Put ur chrome driver path here
WEBPAGE_URL = "https://www.walgreens.com/login.jsp?ru=%2Foffers%2Foffers.jsp"
EMAIL = "" # Put your Walgreens Email here
PASSWORD = "" # Put your Walgreens password here

def create_browser_instance():
    """Create a new Chrome browser instance with specific options."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    prefs = {"profile.default_content_setting_values.geolocation" :2}
    chrome_options.add_experimental_option("prefs",prefs)
    return webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)

def login(browser_driver):
    """Navigate to the login page and enter credentials."""
    browser_driver.get(WEBPAGE_URL)
    time.sleep(2)

    email_input = browser_driver.find_element_by_id("user_name")
    email_input.send_keys(EMAIL)

    password_input = browser_driver.find_element_by_id("user_password")
    time.sleep(2)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

def clip_coupons(browser_driver):
    """Click all 'Clip' buttons on the page."""
    wait = WebDriverWait(browser_driver, 7.5)

    try:
        # Identify the 'Clip' buttons using the CSS class 'btn btn-block btn__blue'
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.btn.btn-block.btn__blue')))
        
        # click all the 'Clip' buttons
        for element in elements:
            browser_driver.execute_script("arguments[0].click();", element)
            time.sleep(2)  # Wait for 2 seconds after each click
            # You may need to handle popups or other interactions after clicking.

    except TimeoutException:
        print("Timed out waiting for page to load")


def main():
    """Main function to coordinate the process."""
    browser_driver = create_browser_instance()
    while True:
        try:
            login(browser_driver)
            time.sleep(10)
            print("Waiting for verification code!")

            if "Access Denied" in browser_driver.page_source:
                print("Access Denied page encountered. Restarting the session...")
                browser_driver.quit()
                browser_driver = create_browser_instance()
                continue

            clip_coupons(browser_driver)
            time.sleep(6)  # Sleep for 6 seconds

        except Exception as e:
            print(f"An error occurred: {e}")
            browser_driver.quit()
            browser_driver = create_browser_instance()

if __name__ == "__main__":
    main()
