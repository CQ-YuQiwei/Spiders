"""
秒杀软件
22:00开抢 时间>=22:00才能抢
打开网址 https://www.taobao.com/
点击登录
点击进入购物车界面 https://cart.taobao.com/cart.htm
全选商品
点击结算
点击条件订单，生成一个订单 代表商品已经抢购了
"""
from selenium import webdriver
import time, datetime


def login():
    # 进入淘宝
    driver.get('https://www.taobao.com/')
    driver.maximize_window()
    # 点击登录
    driver.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()
    # 登录的方式
    # 账号密码
    # driver.find_element_by_id('fm-login-id').send_keys('未出鞘的龙渊')
    # time.sleep(4)
    # driver.find_element_by_id('fm-login-password').send_keys('Qiwei.1105711')
    # # 登录按钮
    # driver.find_element_by_class_name('fm-button').click()
    time.sleep(2)
    driver.get('https://cart.taobao.com/cart.htm')

    now = datetime.datetime.now()
    now2 = now.strftime('%Y-%m-%d %H:%M:%S')
    print('登录成功，当前时间为', now.strftime('%Y-%m-%d %H:%M:%S'))


def buy(times):
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        # 现在的时间要大于抢购的时间
        if now > times:

            # 点击全选
            while True:
                try:
                    if driver.find_element_by_xpath('//*[@id="J_SelectAll2"]'):
                        driver.find_element_by_xpath('//*[@id="J_SelectAll2"]').click()
                        break
                except:
                    print('找不到全选按钮')

            # 点击结算
            while True:
                try:
                    if driver.find_element_by_xpath('//*[@id="J_Go"]'):
                        driver.find_element_by_xpath('//*[@id="J_Go"]').click()
                        break
                except:
                    print('找不到结算按钮')

            # 提交订单
            while True:
                try:
                    if driver.find_element_by_xpath('//*[@id="submitOrderPC_1"]/div[1]/a[2]'):
                        driver.find_element_by_xpath('//*[@id="submitOrderPC_1"]/div[1]/a[2]').click()
                        break
                except:
                    print('找不到提交按钮')


if __name__ == '__main__':
    times = input('请输入抢购的时间：')
    driver = webdriver.Chrome()
    login()
    buy(times)
