#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File: tspider.py
@Description:
@Time: 2021/08/13 20:24:13
@Author: iptoday
@Email: wangdong1221@outlook.com
@Version: 1.0
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

twitter = 'https://twitter.com'

driver = webdriver.Safari()


username_value = ''


def main():
    global driver
    print('开始')
    login()


# 登录
def login():
    driver.get(twitter+'/login')
    global username_value
    username_value = input('请输入用户:\n')
    password_value = input('请输入密码:\n')
    username = driver.find_element_by_name('session[username_or_email]')
    password = driver.find_element_by_name('session[password]')
    username.send_keys(username_value)
    password.send_keys(password_value)
    password.send_keys(Keys.RETURN)
    input('页面若已发生变化，点击任意键继续')
    if driver.current_url.startswith(twitter+'/login'):
        login()
        return
    challenge = None
    try:
        driver.find_element_by_id('challenge_response')
    except:
        pass
    if challenge != None:
        value = input('当前登录用户需要进行验证，请输入验证信息\n')
        challenge.send_keys(value)
        challenge.send_keys(Keys.RETURN)
        input('页面跳转完完成后，点击任意键继续')
    if driver.current_url.startswith('https://twitter.com/home'):
        home()
    while True:
        pass


# 首页
def home():
    print('进入首页')
    print('1、获取关注列表;')
    print('2、获取粉丝列表;')
    print('3、获取主页推文;')
    print('4、获取自己的推文;')
    num = input('请输入想要进行的操作:')
    if num == '1':
        driver.get('%s/%s/following' % (twitter, username_value))
        input('页面跳转完完成后，点击任意键继续')
        has_data = True
        scroll_height = 0
        while has_data:
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(5)
            height = driver.execute_script(
                'return action=document.body.scrollHeight')
            if scroll_height != height:
                scroll_height = height
                print('继续获取新数据')
            else:
                has_data = False
                print('已经滚动到底部, 没有更多数据了')
        divs = driver.find_elements_by_tag_name('div')
        users = []
        for div in divs:
            testid = div.get_attribute('data-testid')
            if testid == 'UserCell':
                users.append(div)
        print('共找到%s个关注' % len(users))
    elif num == '2':
        driver.get('%s/%s/followers' % (twitter, username_value))
    elif num == '4':
        driver.get('%s/%s' % (twitter, username_value))


if __name__ == '__main__':
    main()
