# 编写爬虫，爬取极腾讯防水墙验证码图片，制作深度学习数据集
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import base64
# 开启无头浏览器
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)

# # 实例化浏览器驱动
driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')

# 窗口最大化
# driver.maximize_window()

# 打开网页
url = 'https://007.qq.com/online.html'
driver.get(url)
time.sleep(3)

# 点击可疑用户体验
driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/div/div[2]/div[1]/a[2]').click()
# 点击体验验证码
driver.find_element_by_xpath('//*[@id="code"]').click()
time.sleep(3)
# 获取背景图片
# 根据iframe的id定位到iframe
driver.switch_to.frame('tcaptcha_iframe')
# 通过循环多次获取验证码图片
count = 500
n = 1
for i in range(0, count):

    # 获取到背景图片元素
    im_ele = driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/div[1]/div[2]/img")
    # 获得图片链接地址
    im_url = im_ele.get_attribute('src')
    # print(im_url)
    # requests请求图片链接
    image = requests.get(im_url)
    # # 保存图片到本地
    # with open('tencent.png', 'wb') as f:
    #     f.write(image.content)
    # 保存图片到本地
    with open('tencent/tencent_bg%s.png' % str(i), 'wb') as f:
        f.write(image.content)
    print('第%d张图片保存成功' % i)
    # 刷新验证码
    driver.find_element_by_id('reload').click()

print('运行完毕')
driver.close()
