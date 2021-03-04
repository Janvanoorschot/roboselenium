#!/usr/bin/env python3
import sys
import os
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from selenium import webdriver
from roboload import RoboUser


def work(url):
    driver = webdriver.Chrome("./chromedriver")
    driver.get(url)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Stress the Robomind Academy")
    parser.add_argument("-d", action='store_true', help="enable debug output")
    args = parser.parse_args()
    debug = args.d

    try:
        executor = ThreadPoolExecutor(10)
        loop = asyncio.get_event_loop()
        for url in ["https://google.de"] * 2:
            loop.run_in_executor(executor, work, url)
        loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop)))
    except Exception as e:
        print(f"fatal error: {e}")
