# encoding=utf-8
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def click_next():
    next_page_btn = wait.until(EC.element_to_be_clickable((By.ID, 'mainContent_fycResults_rptPagination_btnPageNext')))
    next_page_btn.click()
    time.sleep(5)


def click_detail(btn):
    print btn
    btn.click()
    time.sleep(5)
    prices = wait.until(EC.element_to_be_clickable((By.ID, 'mainContent_Rates_pnlPricesDetails')))
    driver.back()
    time.sleep(5)


driver = webdriver.PhantomJS()
wait = WebDriverWait(driver, 30)
driver.get('https://www.msccruisesusa.com/en-us/Plan-Book/Find-Cruise.aspx')

page = 0
while True:
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btnCruiseDetail')))
    detail_len = len(driver.find_elements_by_class_name('btnCruiseDetail'))

    for i in range(0, detail_len):
        detail_btn = wait.until(
                EC.element_to_be_clickable((By.ID, 'mainContent_fycResults_rptItin_btnCruiseDetail_' + str(i))))
        click_detail(detail_btn)

    click_next()
    page += 1
    print 'page : ' + str(page) + ' Done!'
