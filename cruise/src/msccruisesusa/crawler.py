# -*- coding: utf-8 -*-

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)


def wait_next_page_btn():
    return wait.until(
            EC.element_to_be_clickable((By.ID, 'mainContent_fycResults_rptPagination_btnPageNext')))


def click_next():
    time.sleep(5)
    wait_next_page_btn().click()
    time.sleep(5)


class Crawler:
    def __init__(self):
        pass

    def run(self, page):
        driver.get('https://www.msccruisesusa.com/en-us/Plan-Book/Find-Cruise.aspx')

        while True:
            wait_next_page_btn()

            items = driver.find_elements_by_class_name('divItin')
            print len(items)

            for item in items:
                months = item.find_elements_by_css_selector('.months>a')
                print len(months)
                if len(months) == 1:
                    self.get_cruise(item)
                    continue

                for i in range(1, len(months)):
                    months[i].click()
                    wait_next_page_btn()
                    self.get_cruise(item)

            click_next()
            print 'page : ' + str(page) + ' Done!'
            page += 1

        return False

    @staticmethod
    def get_cruise(item):
        for cruise in item.find_elements_by_css_selector('.gdvDepartures a'):
            print cruise.get_attribute('cruiseid')
            print cruise.get_attribute('pid')


if __name__ == "__main__":
    Crawler().run(1)
