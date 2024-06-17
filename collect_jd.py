# 编写爬虫，爬取京东验证码图片，制作深度学习数据集
import cv2
import requests
from selenium import webdriver
import time
import base64
from selenium.webdriver import ActionChains

import easing
from locate import detect


# 开启无头浏览器
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)
# 实例化浏览器驱动
driver = webdriver.Chrome("C:\Program Files\Google\Chrome\Application\chromedriver.exe")

# 窗口最大化
# driver.maximize_window()

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


# 通过循环多次获取验证码图片
count = 500
n = 1
for i in range(0, count):
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
    # with open('bg.png', 'wb') as f:
    #     f.write(im_bytes)
    # 保存图片到本地
    with open('jd/jd_bg%s.png' % str(i), 'wb') as f:
        f.write(im_bytes)
    print('第%d张图片保存成功' % i)
    driver.find_element_by_class_name("JDJRV-img-refresh").click()


print('运行完毕')
driver.close()