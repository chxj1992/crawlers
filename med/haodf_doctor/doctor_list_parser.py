#!/usr/bin/python
# encoding: utf-8
import re
import sys

import requests
from bs4 import BeautifulSoup

from med.haodf_doctor import db

reload(sys)
sys.setdefaultencoding('utf8')


class DoctorListParser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        }

    def get_list(self, jibing, page):
        url = 'http://www.haodf.com/jibing/' + str(jibing) + '/daifu_' + str(page) + '_all_all_all_all.htm'

        if db.get_url(url) is not None:
            print 'list ' + url + ' exists'
            return True

        res = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(res.text, 'lxml')
        doctor_list = soup.select('.hp_doc_box_serviceStar')

        if res.status_code != 200 or soup.select_one('.page_cur') is None:
            print 'status code : ' + str(res.status_code) + '. list page error!'
            return False
        if int(soup.select_one('.page_cur').get_text()) < page:
            print 'list page is empty'
            return False

        sql = 'INSERT INTO doctors(`user_id`, `name`, `photo`) VALUES (%s, %s, %s)'
        for doctor in doctor_list:
            doctor_info = doctor.select_one('.oh.zoom.lh180')
            name = doctor_info.select_one('a').get_text().strip()
            user_id = re.compile(r'/doctor/(.*)\.htm').findall(doctor.select_one('a').attrs['href'])[0]
            photo = doctor.select_one('.doctor_photo_serviceStar img').attrs['src']

            try:
                db.execute(sql, [user_id, name, photo])
            except Exception:
                continue
            self.get_detail(user_id)

        db.save_url(url)
        return True

    def get_detail(self, user_id):
        url = 'http://m.haodf.com/touch/doctor/showdoctorinfo?id=' + str(user_id)
        if db.get_url(url) is not None:
            print 'detail ' + url + ' exists'
            return True

        res = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(res.text, 'lxml')

        doctor_info = soup.find_all(class_='ptop_txt')

        title = ''
        if doctor_info[0].find(recursive=False, text=True) is not None:
            title = doctor_info[0].find(recursive=False, text=True)
        level = doctor_info[0].find('span').get_text()

        section = doctor_info[1].find(recursive=False, text=True)
        hospital = doctor_info[1].find('span').get_text()

        skills = re.compile(ur'主治：(.*)').findall(soup.select_one('.wa_iphone').get_text().strip())[0]
        experience = soup.select_one('.con li').get_text().strip()

        sql = 'UPDATE doctors SET `title`=%s,`level`=%s,`section`=%s,`hospital`=%s,`skills`=%s,`experience`=%s WHERE `user_id`=%s'
        try:
            db.execute(sql, [title, level, section, hospital, skills, experience, user_id])
        except Exception:
            print 'set doctor details failed : ' + str(sys.exc_info())
            return False

        db.save_url(url)
        return True


DoctorListParser().get_list('xiaoerganmao', 1)
