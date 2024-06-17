# 编写爬虫，爬取极验验证码图片，制作深度学习数据集

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import base64
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# 开启无头浏览器
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

# # 实例化浏览器驱动
# driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')

# 窗口最大化
# driver.maximize_window()

# 打开网页
url = 'https://captcha1.scrape.center/'
driver.get(url)
time.sleep(3)

# 输入账号密码
driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div[@class='el-col el-col-18 el-col-offset-3']//form["
                             "@class='el-form']/div[1]/div[@class='el-form-item__content']/div/input[@type='text']").send_keys(
    "admin")
driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div[@class='el-col el-col-18 el-col-offset-3']//form["
                             "@class='el-form']/div[2]/div[@class='el-form-item__content']/div/input[@type='password']").send_keys(
    "admin")

# 点击登陆按钮
button = driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div[@class='el-col el-col-18 "
                                      "el-col-offset-3']//form[@class='el-form']//button[@type='button']")
# print(button.text)
# print(button.is_enabled())
button.click()
# wait = WebDriverWait(driver, 5)
# button = wait.until(EC.element_to_be_clickable(
#             (By.CSS_SELECTOR, '.el-button.el-button--primary')))
# button.click()
# 通过循环多次获取验证码图片
count = 500
n = 1
for i in range(430, count):
    time.sleep(5)
    # 获取背景图片
    JS = 'return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");'
    # 执行JS得到图片数据
    im_info = driver.execute_script(JS)
    # 从图片数据中获取图片的base64编码
    im_base64 = im_info.split(',')[1]
    # 将base64编码转换为bytes类型
    im_bytes = base64.b64decode(im_base64)
    # 保存图片到本地
    with open('geetest/geetest_bg%s.png' % str(i), 'wb') as f:
        f.write(im_bytes)
    print('第%d张图片保存成功' % i)
    driver.find_element_by_link_text("刷新验证").click()
    n += 1
    if n == 5:
        time.sleep(3)
        driver.refresh()
        driver.find_element_by_xpath(
            "/html//div[@id='app']/div[2]/div[@class='el-col el-col-18 el-col-offset-3']//form["
            "@class='el-form']/div[1]/div[@class='el-form-item__content']/div/input[@type='text']").send_keys(
            "admin")
        driver.find_element_by_xpath(
            "/html//div[@id='app']/div[2]/div[@class='el-col el-col-18 el-col-offset-3']//form["
            "@class='el-form']/div[2]/div[@class='el-form-item__content']/div/input[@type='password']").send_keys(
            "admin")
        time.sleep(5)
        # button = wait.until(EC.element_to_be_clickable(
        #     (By.CSS_SELECTOR, '.el-button.el-button--primary')))
        # button.click()
        driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div[@class='el-col el-col-18 "
                                     "el-col-offset-3']//form[@class='el-form']//button[@type='button']").click()
        n = 0

print('运行完毕')
driver.close()
