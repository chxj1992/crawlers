#encoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
driver.get("http://weibo.com/login.php")

username = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[node-type='username']")))
username.send_keys("chxj123123@126.com")

password = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[node-type='password']")))
password.send_keys("87822971")

password.send_keys(Keys.RETURN)

time.sleep(10)

driver.get("http://weibo.com/p/1005052794647265/follow?relate=fans&page=1")

wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"ul[node-type='userListBox']")))

fansList = driver.find_elements_by_css_selector("ul[node-type='userListBox'] li")

for fan in fansList:
    print fan.get_attribute("action-data")

driver.close()


