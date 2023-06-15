# 该脚本用于云南大学校园网。检测网络是否连接，如果没有连接则尝试重新连接网络。

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time,datetime

def check_internet():
    url = "http://www.baidu.com"
    timeout = 5
    try:
        _ = requests.get(url, timeout=timeout)

        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"---Internet连接可用。",flush=True)
        return True
    except requests.ConnectionError:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"---Internet连接不可用。",flush=True)
        return False

def reconnect_wifi():
    # 创建一个Firefox选项实例
    options = Options()
    options.add_argument("--headless")  # 启用无头模式

    # 创建一个新的实例
    driver = webdriver.Firefox(executable_path='/home/cyx/MyFiles/geckodriver', options=options,service_log_path='/home/cyx/MyCode/Python/reconnection_wifi/geckodriver.log')  # 这里使用的是Firefox，你也可以改用Chrome或其他浏览器

    retry_count = 0  # 初始化重试计数器
    while retry_count < 3:  # 设置重试次数
        try:
            # 访问网站
            driver.get('校园网登录界面')

            time.sleep(3)  # 延时等待页面加载

            # 输入账号密码
            username = driver.find_element_by_id('username')
            password = driver.find_element_by_id('password')

            time.sleep(1)

            username.send_keys('你的账号')  # 请替换为你的账号
            password.send_keys('你的密码')  # 请替换为你的密码

            time.sleep(1)

            # 点击登录
            login_button = driver.find_element_by_id('login-account')
            login_button.click()

            break  # 如果所有操作都成功，就跳出循环
        except Exception as e:
            print(f"Exception encountered: {e}. Retrying...")
            retry_count += 1  # 如果发生异常，增加重试计数器
            time.sleep(600)  # 等待一段时间再重试

    driver.quit()  # 退出浏览器驱动

while True:  # 无限循环
    if not check_internet():
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"---尝试重新连接网络。",flush=True)
        reconnect_wifi()
        time.sleep(135)  # 暂停
    else:
        time.sleep(135)  # 暂停

