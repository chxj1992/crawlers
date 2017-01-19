#!/usr/bin/python
# encoding: utf-8

import sys

import requests
from bs4 import BeautifulSoup

from med.guahao import db

reload(sys)
sys.setdefaultencoding('utf8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
}

url = 'https://www.guahao.com/search/expert?iSq=&fhc=&fg=0&q=&pi=all&p=%E5%85%A8%E5%9B%BD&ci=all&c=%E4%B8%8D%E9%99%90&o=all&es=all&hl=all&ht=all&hk=all&dt=all&dty=all&hdi=&mf=true&fg=0&ipIsShanghai=false&searchAll=Y&hospitalId=all&standardDepartmentId=all&consult=&volunteerDoctor=&imagetext=&phone=&diagnosis=&sort=&hydate=all&activityId=&weightActivity='
res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.text, 'lxml')

element = soup.select_one('.condition.J_hospitalId')

hospitals = element.select('.J_Submit_A')

sql = "INSERT INTO hospitals (`key`, `name`) VALUES (%s, %s)"
for hospital in hospitals:
    key = hospital.attrs['data-val']
    name = hospital.get_text()
    db.execute(sql, [key, name])

print 'done'
