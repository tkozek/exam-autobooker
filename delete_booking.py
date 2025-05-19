from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import time
import subprocess
from send_email import send_email

from dotenv import load_dotenv
import os

load_dotenv()


MAKE_RESERVATION_BUTTON_CSS_SELECTOR = ".btn.btn-success.btn-sm"
RESERVE_THIS_SESSION_BUTTONS_CSS_SELECTOR = "form button[type='submit'].btn.btn-success.btn-sm"
DELETE_THIS_RESERVATION_BUTTON_CSS_SELECTOR = ".btn.btn-danger.btn-sm"

# Email arguments
subject = "Booking deleted"
body = "Your booking was deleted successfully."
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
    #div[class="container p-0"] div[class=row] 
    existingExamReservationsButton = driver.find_element(By.CSS_SELECTOR, '[data-testid="exam"] a')
    existingExamReservationsButton.click()
    time.sleep(1)  
    changeOrDeleteThisReservationButton = driver.find_element(By.CSS_SELECTOR, MAKE_RESERVATION_BUTTON_CSS_SELECTOR)
    changeOrDeleteThisReservationButton.click()
    time.sleep(1)
    deleteThisReservationButton = driver.find_element(By.CSS_SELECTOR, DELETE_THIS_RESERVATION_BUTTON_CSS_SELECTOR)
    if deleteThisReservationButton:
        deleteThisReservationButton.click()
        time.sleep(1)
        #btn btn-secondary is the cancel button's class
        confirmDeleteReservationButton = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"].btn.btn-danger')
        confirmDeleteReservationButton.click()
        time.sleep(1)
        send_email(subject, body, to_email)
    else:
        print("No such button found :(")
    time.sleep(1000)
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()




