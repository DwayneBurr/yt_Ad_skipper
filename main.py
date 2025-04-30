import os
from selenium import webdriver
import platform
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def get_chrome_userdata():
     system = platform.system()

     if system == "Windows":
        print("opened my chrome")
        return os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
     elif system == "Darwin": #mac os
        print("opened on mac")
        return os.path.expanduser("~/Library/Application Support/Google/Chrome")
     else:
         raise Exception(f"unsopported: {system}")

options = Options()
options.add_argument("--remote-debugging-port=9222")
# options.add_argument("--disable-extensions")
# options.add_argument("--disable-popup-blocking")
# options.add_argument("--disable-gpu")
# # Important: Use *correct* profile
# options.add_argument("--profile-directory=Default")  # or Profile 1, Profile 2

options.add_argument(f"user-data-dir={get_chrome_userdata()}")
options.add_argument("profile-directory=Default")


driver = webdriver.Chrome(options=options)
driver.get("https://www.youtube.com")

assert "YouTube" in driver.title

wait = WebDriverWait(driver, 20)

def accept_cookies():
    accept_cookies = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "yt-spec-touch-feedback-shape--touch-response-inverse")))
    accept_cookies.click()
    print("cookies accepted")

def skip_ad():
    time.sleep(1)

    try:
        while True:
            try:
                    skip_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-skip-ad-button")))
                    skip_button.click()
                    print("Skipped the ad!")
            except Exception as e:
                print("Error while checking for skip button:", e)

            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        driver.quit()

accept_cookies()
skip_ad()
