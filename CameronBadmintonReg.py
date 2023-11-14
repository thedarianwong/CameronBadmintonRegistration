from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os
import boto3
import json 
import traceback
import logging
# Initialize the browser
# Replace with your WebDriver path
# def get_secret(secret_name):
#     # Create a Secrets Manager client
#     client = boto3.client(service_name='secretsmanager', region_name='us-east-1')


#     try:
#         get_secret_value_response = client.get_secret_value(SecretId=secret_name)
#     except client.exceptions.ClientError as e:
#         print(e.response['Error']['Message'])
#         raise e
#     else:
#         secret = get_secret_value_response['SecretString']
#         return json.loads(secret)
# This is the Lambda handler function

### Will implement WebDriver in the later version for better performance
### Would need to create Docker for EC2/ECS since script broken in Lambda due to PipeErrno32

def open_browser_and_navigate(url):
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument("--headless")  # Ensure GUI is off
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument('--single-process')
    options.add_argument('--window-size=1920,1080')
    browser = webdriver.Chrome('/opt/chromedriver', options = options)
    browser.get(url)
    return browser


def enroll_now(browser):
    try:
        button = browser.find_element(
            "xpath", '//*[@id="main-content-body"]/div[1]/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/button')
        button.click()
        time.sleep(3)
        print("Enroll button works.")
    except NoSuchElementException:
        print("Enroll button not found.")
        browser.quit()


def login(browser, username, password):
    try:
        username_field = browser.find_element(
            "xpath", '//*[@id="main-content-body"]/div[1]/div[3]/div/div/div/div[1]/div[2]/input')
        username_field.send_keys(username)
        time.sleep(1)
        password_field = browser.find_element(
            "xpath", '//*[@id="main-content-body"]/div[1]/div[3]/div/div/div/div[2]/div[2]/input')
        password_field.send_keys(password)
        time.sleep(1)
        login_button = browser.find_element(
            "xpath", '//*[@id="main-content-body"]/div[1]/div[3]/div/div/div/div[4]/button')
        login_button.click()
        time.sleep(5)
        print("Log in button works.")
    except Exception as e:
        print(f"An error occurred: {e}")
        browser.quit()



def add_to_cart(browser):
    try:
        time.sleep(5)
        dropdown_option = browser.find_element(By.CLASS_NAME,'activity-enrollform__dropdown-wrapper')
        dropdown_option.click()
        print("Found dropdown")
        time.sleep(5)
        option_xpath = f"//li[@title='Darian Wong']"
        option = browser.find_element("xpath", option_xpath)
        option.click()
        print("Found participant")
        time.sleep(10)
        dropdown_add_to_cart = browser.find_element("xpath",  '//*[@id="main-content-body"]/div[1]/div[3]/div/div[1]/div/div[2]/div/div[2]/div[1]/div/button')
        dropdown_add_to_cart.click()
        print("Add to cart button works.")
    except NoSuchElementException as e:
        logging.error("Element not found: %s", e)
        browser.quit()



def submit(browser):
    try:
        time.sleep(3)
        finish = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content-body"]/div[1]/div[3]/div/div[1]/div/div/div[2]/div/div[2]/div[1]/div/button')))
        finish.click()
        print("Submit button works.")
        time.sleep(3)
    except NoSuchElementException as e:
        logging.error("Submit button not found: %s", e)
    finally:
        browser.quit()


def main():
    try:
        url = ('https://anc.ca.apm.activecommunities.com/burnaby/activity/search?onlineSiteId=0&days_of_week=0000010&activity_select_param=2&center_ids=40&activity_keyword=badminton%20reserve&viewMode=list')
        username = 'USERNAME'
        password = 'PASSWORD'
        browser = open_browser_and_navigate(url)
        enroll_now(browser)
        login(browser, username, password)
        add_to_cart(browser)
        submit(browser)
    except Exception as e:
        print(f"An error occurred in main: {e}")
    finally:
        if browser:
            browser.quit()

def lambda_handler(event, context):
    try:
        main()
        # Check if Lambda is working
        return {
            'statusCode': 200,
            'body': json.dumps('Badminton script executed successfully!')
        }
    except Exception as e:
        traceback_string = traceback.format_exc()
        print(traceback_string)
        error_response = {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'trace': traceback_string
            })
        }
        return error_response


if __name__ == "__main__":
    main()
