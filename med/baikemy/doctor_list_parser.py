#!/usr/bin/python
# encoding: utf-8
import re
import sys

import requests
from bs4 import BeautifulSoup

from med.baikemy import db


class DoctorListParser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        }

    def get_list(self, page):
        url = 'http://www.baikemy.com/doctor/list/0_0/0_0/0_0?pageIndex=' + str(page)

        if db.get_url(url) is not None:
            print 'list ' + url + ' exists'
            return True

        res = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(res.text, 'lxml')
        doctor_list = soup.select('.y_expert .yiy_lz_im')

        if len(doctor_list) == 0:
            print 'list page is empty'
            return False

        sql = 'INSERT INTO doctors(`user_id`, `name`, `title`, `hospital`, `section`, `photo`) VALUES (%s, %s, %s, %s, %s, %s)'
        for doctor in doctor_list:
            name = doctor.find(class_="yiy_expert_name").get_text()

            doctor_info = doctor.select(".yiy_expert_desc p")

            title = re.compile(ur'\xa0(\S+)').findall(doctor_info[0].get_text())[0]
            hospital = doctor_info[1].get_text().strip()
            section = doctor_info[2].get_text().strip()

            href = doctor.select_one('.yiy_expert_avatar a').attrs['href']
            user_id = re.compile(r'(\w+)\.baikemy\.com').findall(href)[0]
            photo = doctor.select_one('.yiy_expert_avatar img').attrs['src']

            try:
                db.execute(sql, [user_id, name, title, hospital, section, photo])
            except Exception:
                continue
            self.get_detail(user_id)

        db.save_url(url)
        return True

    def get_detail(self, user_id):
        url = 'http://' + user_id + '.baikemy.com/expert/profile'
        if db.get_url(url) is not None:
            print 'detail ' + url + ' exists'
            return True

        res = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(res.text, 'lxml')
        doctor_detail = soup.select('.zjgzsym_rrong_left_four_zj')
        intro, skills = '', ''
        if len(doctor_detail) > 0:
            intro = doctor_detail[0].get_text().strip()
        if len(doctor_detail) > 1:
            skills = doctor_detail[1].get_text().strip()

        sql = 'UPDATE doctors SET `intro`=%s,`skills`=%s WHERE `user_id`=%s'
        try:
            db.execute(sql, [intro, skills, user_id])
        except Exception:
            print 'set doctor details failed : ' + sys.exc_info()[0]
            return False

        db.save_url(url)
        return True


DoctorListParser().get_list(1)
