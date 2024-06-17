import random

import cv2
from selenium import webdriver
import time
import base64

from selenium.common.exceptions import NoSuchElementException
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

# 输入账号密码
driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div[@class='el-col el-col-18 el-col-offset-3']//form["
                             "@class='el-form']/div[1]/div[@class='el-form-item__content']/div/input[@type='text']").send_keys(
    "admin")
driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div[@class='el-col el-col-18 el-col-offset-3']//form["
                             "@class='el-form']/div[2]/div[@class='el-form-item__content']/div/input[@type='password']").send_keys(
    "admin")
time.sleep(5)
# 点击登陆按钮
button = driver.find_element_by_css_selector(".el-button.el-button--primary")
# print(button.text)
# print(button.is_enabled())
button.click()
time.sleep(2)


def save_bg(driver):
    # 获取背景图片
    js = "return document.getElementsByClassName('geetest_canvas_bg geetest_absolute')[0].toDataURL('image/jpeg');"
    # 执行JS得到图片数据
    im_info = driver.execute_script(js)
    # 从图片数据中获取图片的base64编码
    im_base64 = im_info.split(',')[1]
    # 将base64编码转换为bytes类型
    im_bytes = base64.b64decode(im_base64)
    # 保存图片到本地
    with open('bg.png', 'wb') as f:
        f.write(im_bytes)


# 识别背景图片中缺口位置

# # 输出识别结果信息
# img = cv2.imread('bg.png')
# # 调用detect函数进行识别
# location = detect(img)
# print(location[0])
# # 输出缺口位置坐标
# xywh = location[0]['position']
# print(xywh)
# # 输出缺口到左边缘的距离，即左上点的y坐标
# x = xywh[0]
# print(x)

def identify(path):
    # 设置背景图片路径
    # path = "bg.png"
    # 调用roboflow api进行识别
    # 获得识别信息
    info = detect_api(path)
    predictions = info['predictions']
    print(predictions[0])
    # 获取x坐标
    x = predictions[0]['x']
    print(x)
    w = predictions[0]['width']
    print(w)
    return x - w / 2


# 拖动滑块到缺口位置
def drag_slide(driver):
    # 获取滑块拖动按钮元素
    button = driver.find_element_by_class_name('geetest_slider_button')

    # 使用detect函数时使用的offset
    # offset = x - 5
    # 调用api时使用的offset
    # offset = x - w / 2

    offset = identify('bg.png') - 5
    offsets, tracks = easing.get_tracks(offset, 6, 'ease_in_out_back')

    back_step = round(random.uniform(1, 5))
    pause_time = round(random.random())
    ActionChains(driver).click_and_hold(button).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(x, 0).perform()
    # ActionChains(driver).move_by_offset(-back_step, 0).perform()
    ActionChains(driver).pause(pause_time).release().perform()


def isElementExist(name):
    try:
        element = driver.find_element_by_class_name(name)
        return True
    except NoSuchElementException as e:
        return False


while True:
    # 保存背景图片
    save_bg(driver)
    # 识别背景图片中缺口位置
    identify('bg.png')
    # 拖动滑块到缺口位置
    drag_slide(driver)
    time.sleep(2)

    if driver.current_url == url:
        print("验证失败")
        flag = isElementExist("geetest_panel_error_content")
        if flag == True:
            driver.find_element_by_class_name("geetest_panel_error_content").click()
            time.sleep(2)
        else:
            # 刷新验证码
            driver.find_element_by_link_text("刷新验证").click()
        # 保存背景图片
        save_bg(driver)
        # 识别背景图片中缺口位置
        identify('bg.png')
        # 拖动滑块到缺口位置
        drag_slide(driver)
        time.sleep(2)
    else:
        print("验证成功")
        break

