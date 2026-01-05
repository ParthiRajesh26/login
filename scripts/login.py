#!/usr/bin/env python3
import os
import sys
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_env_var(var_name):
    value = os.environ.get(var_name)
    if not value:
        logging.error(f"Missing required environment variable: {var_name}")
        sys.exit(1)
    return value

def setup_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def main():
    logger = setup_logger()

    url = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login'
    username = get_env_var('LOGIN_USERNAME')
    password = get_env_var('LOGIN_PASSWORD')

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as e:
        logger.error(f"Failed to start Chrome WebDriver: {e}")
        sys.exit(1)

    try:
        logger.info(f"Navigating to {url}")
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        # Wait for the username field
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        login_button.click()

        # Wait for dashboard or successful login element
        dashboard_locator = (By.XPATH, "//h6[text()='Dashboard']")
        wait.until(EC.presence_of_element_located(dashboard_locator))
        logger.info("Login successful. Dashboard loaded.")
    except (NoSuchElementException, TimeoutException) as e:
        logger.error(f"Login failed: {e}")
        sys.exit(2)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(3)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
