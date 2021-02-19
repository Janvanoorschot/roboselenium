#!/usr/bin/env python3
import sys
import os
import argparse
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(rootdir)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

op = webdriver.ChromeOptions()
# remove the next line if you want to see what is happening
op.add_argument('headless')
browser = webdriver.Chrome(executable_path=os.path.join(rootdir, "./drivers/chromedriver"), options=op)
browser.get('http://www.google.com')
sleep(5)
browser.quit()

