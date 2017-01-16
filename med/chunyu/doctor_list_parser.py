#!/usr/bin/python
# encoding: utf-8
import re
import sys

import requests
from bs4 import BeautifulSoup

from med.chunyu import db


class DoctorListParser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        }

    def get_list(self, section_id, page):
        url = 'http://www.chunyuyisheng.com/clinics/' + str(section_id) + '/doctors?page=' + str(page)

        if db.get_url(url) is not None:
            print 'list ' + url + ' exists'
            return True

        res = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(res.text, 'lxml')
        doctor_list = soup.select('#doctorsList .docCell')

        if len(doctor_list) == 0:
            print 'list page is empty'
            return False

        sql = 'INSERT INTO doctors(`user_id`, `name`, `title`, `hospital`, `section`, `photo`,  `skills`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        for doctor in doctor_list:
            name = doctor.find(class_="docName").get_text()
            doctor_info = doctor.find(class_="bdSubHd").get_text().replace(u'\xa0', ' ')
            doctor_info = re.compile(ur'\S+').findall(doctor_info)
            title = doctor_info[0]
            hospital = doctor_info[1]
            section = doctor_info[2]
            user_id = re.compile(r'/doctor/(\w+)').findall(doctor.find(class_='docAvatar').attrs['href'])[0]
            photo = doctor.select_one('.docAvatar img').attrs['src']
            skills = doctor.find(class_='professional').get_text()
            try:
                db.execute(sql, [user_id, name, title, hospital, section, photo, skills])
            except Exception:
                continue
            self.get_detail(user_id)

        db.save_url(url)
        return True

    def get_detail(self, user_id):
        url = 'http://www.chunyuyisheng.com/doctor/' + user_id
        if db.get_url(url) is not None:
            print 'detail ' + url + ' exists'
            return True

        print user_id
        res = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(res.text, 'lxml')
        doctor_detail = soup.select('.otherInfoCnt')
        intro, workplace = '', ''
        if len(doctor_detail) > 1:
            intro = doctor_detail[1].get_text().strip()
        if len(doctor_detail) > 2:
            workplace = doctor_detail[2].get_text().strip()

        sql = 'UPDATE doctors SET `intro`=%s,`workplace`=%s WHERE `user_id`=%s'
        try:
            db.execute(sql, [intro, workplace, user_id])
        except Exception:
            print 'set doctor details failed : ' + sys.exc_info()[0]
            return False

        db.save_url(url)
        return True

# DoctorListParser().get_list(1, 1)
