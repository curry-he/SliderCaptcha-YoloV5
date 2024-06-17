# 编写爬虫，爬取网易易盾验证码图片，制作深度学习数据集
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import base64
# 开启无头浏览器
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

# # 实例化浏览器驱动
# driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')

# 窗口最大化
driver.maximize_window()

# 打开易盾网页，进入滑块验证码体验界面
url = 'https://dun.163.com/trial/jigsaw'
driver.get(url)
time.sleep(3)

# 点击弹出式体验（这里必须要使窗口最大化）
driver.find_element_by_xpath("/html//div[@class='g-bd']/div[@class='g-in g-in-top']//ul["
                             "@class='tcapt-tabs__container']/li[.='弹出式']").click()
# 点击登陆
driver.find_element_by_xpath("/html//div[@class='g-bd']/div[@class='g-in g-in-top']/div[@class='g-mn2']/div["
                             "@class='m-tcapt']//div[@class='tcapt_wrap tcapt_wrap--pop']//button[.='登录']").click()
time.sleep(3)
# 获取背景图片
# 根据iframe的id定位到iframe
# driver.switch_to.frame('tcaptcha_iframe')
# 通过循环多次获取验证码图片
count = 500
n = 1
for i in range(0, count):
    time.sleep(3)
    # 获取到背景图片元素
    im_ele = driver.find_element_by_class_name('yidun_bg-img')
    # 获得图片链接地址
    im_url = im_ele.get_attribute('src')
    # print(im_url)
    # requests请求图片链接
    image = requests.get(im_url)
    # 保存图片到本地
    # with open('yidun.png', 'wb') as f:
    #     f.write(image.content)
    # 保存图片到本地
    with open('yidun/yidun_bg%s.png' % str(i), 'wb') as f:
        f.write(image.content)
    print('第%d张图片保存成功' % i)
    # 刷新验证码
    driver.find_element_by_class_name('yidun_refresh').click()

print('运行完毕')
# driver.close()
