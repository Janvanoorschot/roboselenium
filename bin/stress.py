#!/usr/bin/env python3
import sys
import os
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from selenium import webdriver

from roboload import RoboUser
from roboload.users_data import users


def work(ix, url, repeat=1):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(executable_path=os.path.join(rootdir, "drivers/chromedriver"), options=op)
        user = RoboUser(driver, url, users[ix][0], users[ix][1])
        for jx in range(repeat):
            try:
                print(f"!!!START[{ix}/{jx}]!!!")
                user.run_101()
                print(f"!!!YES[{ix}/{jx}]!!!!")
            except Exception as e:
                print(f"!!!NO[{ix}/{jx}]!!!!:{e}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Stress the Robomind Academy")
    parser.add_argument("-d", action='store_true', help="enable debug output")
    args = parser.parse_args()
    debug = args.d

    try:
        executor = ThreadPoolExecutor(10)
        loop = asyncio.get_event_loop()
        urls = ["http://localhost:8080"] * 8
        for ix in range(len(urls)):
            url = urls[ix]
            loop.run_in_executor(executor, work, ix, url, 50)
        loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop)))
    except Exception as e:
        print(f"fatal error: {e}")
