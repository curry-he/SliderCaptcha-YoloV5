from selenium.common.exceptions import NoSuchElementException
import random

import cv2
from selenium import webdriver
import time
import base64
from selenium.webdriver import ActionChains

import easing
# from locate import detect
from api import detect_api

# 实例化浏览器驱动
driver = webdriver.Chrome("C:\Program Files\Google\Chrome\Application\chromedriver.exe")

# 窗口最大化
# driver.maximize_window()

# 打开网页
url = 'https://captcha1.scrape.center/'
driver.get(url)
time.sleep(2)


def isElementExist(name):
    try:
        element = driver.find_element_by_class_name(name)
        return True
    except NoSuchElementException as e:
        return False


a = isElementExist("geetest_panel_error_content")
print(a)