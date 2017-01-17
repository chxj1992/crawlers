#!/usr/bin/python
# encoding: utf-8
import re
import sys

import requests
from bs4 import BeautifulSoup

from med.myzd import db


class DoctorListParser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        }

    def get_list(self, section_id, page):
        url = 'http://www.mingyizhudao.com/doctor-top-disease_sub_category-' + str(section_id) \
              + '-disease-0-city-0-mtitle-0-page-' + str(page) + '-getcount-1.html'

        if db.get_url(url) is not None:
            print 'list ' + url + ' exists'
            return True

        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf8'
        soup = BeautifulSoup(res.text, 'lxml')

        doctor_list = soup.select('#doctorList .col-lg-3.col-sm-4.mt30')

        if len(doctor_list) == 0:
            print 'list page is empty'
            return False

        sql = 'INSERT INTO doctors(`user_id`, `name`, `title`, `level`, `hospital`, `section`, `photo`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        for doctor in doctor_list:
            doctor_info = doctor.select('.text-center span')
            name = doctor_info[0].get_text()

            title_info = doctor_info[1].get_text().replace(u'\xa0', ' ')
            title_info = re.compile(ur'\S+').findall(title_info)
            title, level = '', ''
            if len(title_info) > 0:
                title = title_info[0]
            if len(title_info) > 1:
                level = title_info[1]

            user_id = re.compile(r'/doctor/(\w+)').findall(doctor.find('a').attrs['href'])[0]
            photo = doctor.select_one('.border-radius img').attrs['src']

            doctor_info = doctor.select('div.text-center.mt5')

            section = doctor_info[0].get_text()
            hospital = doctor_info[1].get_text()

            try:
                db.execute(sql, [user_id, name, title, level, hospital, section, photo])
            except Exception:
                continue

            self.get_detail(user_id)

        db.save_url(url)
        return True

    def get_detail(self, user_id):
        url = 'http://www.mingyizhudao.com/doctor/' + user_id
        if db.get_url(url) is not None:
            print 'detail ' + url + ' exists'
            return True

        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf8'
        soup = BeautifulSoup(res.text, 'lxml')
        doctor_detail = soup.select_one('.col-sm-8.pr5')

        recommend, skills, experience, honor = '', '', '', ''

        if len(doctor_detail.select('.recommend-reason1')) > 0:
            recommend = ','.join(map(lambda x: x.get_text().strip(), doctor_detail.select('.recommend-reason1')))
        if doctor_detail.select_one('.disTags ul') is not None:
            skills = doctor_detail.select_one('.disTags ul').get_text().strip()
        if doctor_detail.select_one('.experience-text') is not None:
            experience = doctor_detail.select_one('.experience-text').get_text().strip()
        if len(doctor_detail.select('.honour li')) > 0:
            honor = ','.join(map(lambda x: x.get_text().strip(), doctor_detail.select('.honour li')))

        sql = 'UPDATE doctors SET `recommend`=%s,`skills`=%s,`experience`=%s,`honor`=%s WHERE `user_id`=%s'
        try:
            db.execute(sql, [recommend, skills, experience, honor, user_id])
        except Exception:
            print 'set doctor details failed : ' + sys.exc_info()[0]
            return False

        db.save_url(url)
        return True


DoctorListParser().get_list(101, 1)
