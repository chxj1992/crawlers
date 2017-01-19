#!/usr/bin/python
# encoding: utf-8
import re
import sys

import requests
from bs4 import BeautifulSoup

from med.guahao import db

reload(sys)
sys.setdefaultencoding('utf8')


class DoctorListParser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        }

    def get_list(self, hospital_id, section_id, page):
        url = 'https://www.guahao.com/search/expert?iSq=&fhc=&fg=0&q=&pi=all&p=%E5%85%A8%E5%9B%BD&ci=all&c=%E4%B8%8D%E9%99%90&o=all&es=all&hl=all&ht=all&hk=all&dt=all&dty=all&hdi=&mf=true&fg=0&ipIsShanghai=false&searchAll=Y&hospitalId=' \
              + hospital_id + '&standardDepartmentId=' \
              + section_id \
              + '&consult=&volunteerDoctor=&imagetext=&phone=&diagnosis=&sort=&hydate=all&activityId=&weightActivity=&pageNo=' \
              + str(page)

        if page > 60:
            print 'list page is empty'
            return False

        if db.get_url(url) is not None:
            print 'list ' + url + ' exists'
            return True

        res = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'lxml')

        if soup.select_one('.current') is None or int(soup.select_one('.current').get_text()) != page:
            print 'list page is empty'
            return False

        print url

        doctor_list = soup.select('.g-doctor-item')

        sql = 'INSERT INTO doctors(`user_id`, `name`, `title`, `hospital`, `section`, `photo`) VALUES (%s, %s, %s, %s, %s, %s)'
        for doctor in doctor_list:
            user_id = doctor.select_one('a').attrs['monitor-doctor-id']
            img = doctor.select_one('img')
            photo = img.attrs['src']
            basic_info = re.compile(ur'\S+').findall(doctor.find('dt').get_text().strip().replace(u'\xa0', ' '))
            name = basic_info[0]

            title = ''
            if len(basic_info) > 1:
                title = basic_info[1]

            dd = doctor.select('dd a')
            section = dd[0].get_text().strip()
            hospital = dd[1].get_text().strip()

            try:
                db.execute(sql, [user_id, name, title, hospital, section, photo])
            except Exception:
                continue
            self.get_detail(user_id)

        db.save_url(url)
        return True

    def get_detail(self, user_id):
        url = 'https://www.guahao.com/expert/' + user_id
        if db.get_url(url) is not None:
            print 'detail ' + url + ' exists'
            return True

        res = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(res.text, 'lxml')
        doctor_detail = soup.select_one('.detail.word-break')

        if doctor_detail is None:
            print 'doctor '+user_id + ' not exists'
            return False

        print url

        level, intro, skills = '', '', ''

        if len(doctor_detail.find('h1').select('span')) > 2:
            level = doctor_detail.find('h1').select('span')[2].get_text().strip()

        if doctor_detail.select_one('.goodat a'):
            skills = doctor_detail.select_one('.goodat a').attrs['data-description']
        elif doctor_detail.select_one('.goodat span'):
            skills = doctor_detail.select_one('.goodat span').get_text().strip()

        if doctor_detail.select_one('.about a'):
            intro = doctor_detail.select_one('.about a').attrs['data-description']
        elif doctor_detail.select_one('.about span'):
            intro = doctor_detail.select_one('.about span').get_text().strip()

        sql = 'UPDATE doctors SET `level`=%s,`intro`=%s,`skills`=%s WHERE `user_id`=%s'
        try:
            db.execute(sql, [level, intro, skills, user_id])
        except Exception:
            print 'set doctor details failed : ' + str(sys.exc_info())
            return False

        db.save_url(url)
        return True

DoctorListParser().get_list('c9c2f720-93d3-4247-90df-5e673ccead60000', '7f67c1f6-cff3-11e1-831f-5cf9dd2e7135', 1)
