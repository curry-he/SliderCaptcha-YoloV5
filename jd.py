import random

import cv2
import requests
from selenium import webdriver
import time
import base64
from selenium.webdriver import ActionChains

import easing
from locate import detect

# 实例化浏览器驱动
driver = webdriver.Chrome("C:\Program Files\Google\Chrome\Application\chromedriver.exe")

# 窗口最大化
driver.maximize_window()

# 打开网页
url = 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F%3Fcountry%3DUSA'
driver.get(url)
driver.find_element_by_link_text("账户登录").click()
time.sleep(3)

# 输入账号密码
driver.find_element_by_id("loginname").send_keys("admin")
driver.find_element_by_id("nloginpwd").send_keys("admin")
time.sleep(2)
# 点击登陆按钮
button = driver.find_element_by_id("loginsubmit")
# print(button.text)
# print(button.is_enabled())
button.click()

time.sleep(2)
# 获取背景图片
# 获取到背景图片元素
im_ele = driver.find_element_by_css_selector(".JDJRV-bigimg > img")
# 获得图片链接地址
im_info = im_ele.get_attribute('src')
im_base64 = im_info.split(',')[1]
# print(im_base64)
# 将base64编码转换为bytes类型
im_bytes = base64.b64decode(im_base64)
# 保存图片到本地
with open('bg.png', 'wb') as f:
    f.write(im_bytes)

# 识别背景图片中缺口位置

# 输出识别结果信息
img = cv2.imread('bg.png')
location = detect(img)
print(location[0])
# 输出缺口位置坐标
xywh = location[0]['position']
print(xywh)
# 输出缺口到左边缘的距离，即左上点的y坐标
x = xywh[0]
print(x)

w = xywh[2]
print(w)

time.sleep(2)
# 拖动滑块到缺口位置
# 获取滑块拖动按钮元素
button = driver.find_element_by_xpath("/html//div[@id='JDJRV-wrap-loginsubmit']/div/div/div/div[2]/div[3]")
offset = (x * 278 / 360) + w / 38.6
offsets, tracks = easing.get_tracks(offset, 12, 'ease_in_out_back')

back_step = round(random.uniform(1, 5))
pause_time = round(random.random())
ActionChains(driver).click_and_hold(button).perform()
for x in tracks:
    ActionChains(driver).move_by_offset(x, 0).perform()
ActionChains(driver).move_by_offset(-back_step, 0).perform()
ActionChains(driver).pause(pause_time).release().perform()
