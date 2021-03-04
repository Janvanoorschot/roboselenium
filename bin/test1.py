#!/usr/bin/env python3
import sys
import os
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(rootdir)

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from time import sleep


class element_has_css_class(object):
    """An expectation for checking that an element has a particular css class.

    locator - used to find the element
    returns the WebElement once it has the particular css class
    """
    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False


op = webdriver.ChromeOptions()
# remove the next line if you want to see what is happening
# op.add_argument('headless')
browser = webdriver.Chrome(executable_path=os.path.join(rootdir, "./drivers/chromedriver"), options=op)


browser.get("http://localhost:8080/login/auth")
# page should be ready, click on the login
browser.find_element_by_id("username").send_keys("team27/jan@janvanoorschot.nl")
browser.find_element_by_id("password").send_keys("h622p")
browser.find_element_by_id("submit").click()

# wait for the target page (and we do not know which, but probably the profile page)
try:
    myElem = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, 'profileForm')))
except TimeoutException:
    browser.quit()

# go to the Challenge
browser.get("http://localhost:8080/course/robomind/Basis_1/Getting%20started/1")

# fill the script and start it
script = "forward(2)"
codeMirror = browser.find_element_by_class_name('CodeMirror')
browser.execute_script("arguments[0].CodeMirror.setValue(\"" + script + "\");", codeMirror)
sleep(1)
runButton = browser.find_element_by_name('idButtonA')
browser.execute_script("arguments[0].click();", runButton)

# wait for the script to run
try:
    WebDriverWait(browser, 10).until(element_has_css_class((By.ID, 'myrobomindide'), "RunModeRunning"))
except TimeoutException:
    print("stopped")
# wait for the script to be done
try:
    WebDriverWait(browser, 10).until(element_has_css_class((By.ID, 'myrobomindide'), "RunModeStopped"))
except TimeoutException:
    browser.quit()
# logout
browser.execute_script("document['hiddenLogoutForm'].submit();", runButton)

# wait for the home page
# wait for the target page (and we do not know which, but probably the profile page)
try:
    myElem = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'videoMsg')))
except TimeoutException:
    browser.quit()

browser.quit()


