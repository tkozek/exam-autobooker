from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import subprocess
from send_email import send_email

from dotenv import load_dotenv
import os

load_dotenv()

MAKE_RESERVATION_BUTTON_CSS_SELECTOR = ".btn.btn-success.btn-sm"
RESERVE_THIS_SESSION_BUTTONS_CSS_SELECTOR = "form button[type='submit'].btn.btn-success.btn-sm"
DELETE_THIS_RESERVATION_BUTTON_CSS_SELECTOR = ".btn.btn-danger"

# Email arguments
subject = "Booking confirmed"
body = "Your booking was successful."
to_email = os.getenv(TO_EMAIL)
#
service = Service(os.getenv(PATH_TO_CHROME_DRIVER))

# Set Chrome options
options = ChromeOptions()
options.add_argument(os.getenv(USER_DATA_DIR))
options.add_argument("profile-directory=default") 

options.add_argument("--headless=new")

driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://us.prairietest.com/pt")
    time.sleep(1)  
    makeAReservationButton = driver.find_element(By.CSS_SELECTOR, ".btn.btn-success.btn-sm")
    makeAReservationButton.click()
    time.sleep(1)

    reserveThisSessionButtons = driver.find_elements(By.CSS_SELECTOR, "form button[type='submit'].btn.btn-success.btn-sm")
    if reserveThisSessionButtons:
        reserveButton = reserveThisSessionButtons[-1]
        driver.maximize_window()
        driver.execute_script("arguments[0].scrollIntoView(true);", reserveButton)
        time.sleep(0.5)
        reserveButton.click()
        time.sleep(1)
        send_email(subject, body, to_email)
    else:
        print("No such button found :(")
    time.sleep(5)
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()




