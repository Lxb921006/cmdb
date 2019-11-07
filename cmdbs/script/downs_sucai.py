#!/usr/bin/env python3
# coding:       utf-8
# Name:         downs_sucai
# Date:         2019/8/17
# Author:       xuanbiao
# Description:  

import requests
import json
import re
import os
import queue
import time
import random
import threading
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import request
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def login():
    info = DesiredCapabilities.CHROME
    info['loggingPrefs'] = {'performance': 'ALL'}
    browser = webdriver.Chrome(
        executable_path=r'G:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
        desired_capabilities=info
    )
    browser.get('https://passport.csdn.net/login')
    html = browser.page_source
    browser.quit()
    return html


if __name__ == '__main__':
    print(login())
