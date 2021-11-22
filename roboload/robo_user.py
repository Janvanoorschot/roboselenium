from urllib.parse import urljoin
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class RoboUser:

    def __init__(self, driver, url, user, password):
        self.driver = driver
        self.url = url
        self.user = user
        self.password = password

    def login(self):
        loginurl = urljoin(self.url, "login/auth")
        self.driver.get(loginurl)
        self.driver.find_element_by_id("username").send_keys(self.user)
        self.driver.find_element_by_id("password").send_keys(self.password)
        self.driver.find_element_by_id("submit").click()
        try:
            myElem = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, 'profileForm')))
        except TimeoutException:
            raise RuntimeError("profile page did not appear after login")

    def logout(self):
        self.driver.execute_script("document['hiddenLogoutForm'].submit();")
        try:
            myElem = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'videoMsg')))
        except TimeoutException:
            raise RuntimeError("no homepage after logout")

    def jump(self, url):
        challenge_url = urljoin(self.url, url)
        self.driver.get(challenge_url)

    def runscript(self, script):
        codeMirror = self.driver.find_element_by_class_name('CodeMirror')
        self.driver.execute_script("arguments[0].CodeMirror.setValue(\"" + script + "\");", codeMirror)
        sleep(0.5)
        runButton = self.driver.find_element_by_name('idButtonA')
        self.driver.execute_script("arguments[0].click();", runButton)
        # wait for the script to run
        try:
            messagespane = self.driver.find_element_by_class_name('messagespane')
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element(messagespane))
            # WebDriverWait(self.driver, 20).until(element_has_css_class((By.ID, 'myrobomindide'), "RunModeRunning"))
        except TimeoutException:
            raise RuntimeError("script did not start")
        # wait for the script to be done
        try:
            messagespane = self.driver.find_element_by_class_name('messagespane')
            WebDriverWait(self.driver, 10).until(EC.visibility_of(messagespane))
            # WebDriverWait(self.driver, 10).until(element_has_css_class((By.ID, 'myrobomindide'), "RunModeStopped"))
        except TimeoutException:
            raise RuntimeError("script did not stop")


    def run_101(self):
        self.login()
        self.jump("course/robomind/Basis_1/Getting%20started/1")
        self.runscript("forward(1)")
        self.logout()


class element_has_css_class(object):
    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False
