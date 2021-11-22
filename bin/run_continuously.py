#!/usr/bin/env python3
#
# Run every so often and send email when the Robomind
# site stops responding. It will send another email
# when the site starts again.
#
import os
import time
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from roboload import RoboUser
from roboload.users_data import users


def work(url):
    op = webdriver.ChromeOptions()
    ser = Service(os.path.join(rootdir, "/usr/local/bin/chromedriver"))
    op.add_argument('headless')
    driver = webdriver.Chrome(service=ser, options=op)
    user = RoboUser(driver, url, users[0][0], users[0][1])
    try:
        try:
            user.run_101()
        except Exception as e:
            pass
    finally:
        driver.quit()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Keep an eye on the Robomind Academy")
    parser.add_argument("-d", action='store_true', help="enable debug output")
    args = parser.parse_args()
    debug = args.d

    try:
        url = "https://www.robomindacademy.com"
        work(url)
    except Exception as e:
        print(f"fatal error: {e}")
