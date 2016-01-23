# encoding=utf-8
from selenium import webdriver

driver = webdriver.Firefox()

driver.get("http://i.baidu.com/")
driver.delete_all_cookies()

cookieStr = open("cookie.txt").read().strip()
cookieList = cookieStr.split(';')

for cookie in cookieList:
    cookieArr = cookie.split('=')
    cookieObj = {'name': cookieArr[0], 'value': cookieArr[1]}
    driver.add_cookie(cookieObj)

driver.refresh()
