import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

SIGN_IN_PAGE = 'https://mybdjobs.bdjobs.com/mybdjobs/signin.asp'
USERNAME = 'ratnabiswas11'
PASSWORD = '10301030'

driver = webdriver.Chrome('chromedriver.exe')

# Getting log in page
driver.get(SIGN_IN_PAGE)
time.sleep(5)

# Closing ad modal
close_modal_button = driver.find_element(By.XPATH, '//div[@class="modal-content"]/a')
close_modal_button.click()

# Fill up username
username_field = driver.find_element(By.ID, 'TXTUSERNAME')
sign_in_next_button = driver.find_element(By.XPATH, '//input[@class="btn btn-success btn-signin"]')
username_field.send_keys(USERNAME)
sign_in_next_button.click()
time.sleep(3)

# Fill up password
password_field = driver.find_element(By.ID, 'TXTPASS')
sign_in_complete_button = driver.find_element(By.XPATH, '//input[@class="btn btn-success btn-signin"]')
password_field.send_keys(PASSWORD)
sign_in_complete_button.click()
time.sleep(3)

# Go to Edit resume page
EDIT_RESUME_LINK = 'https://mybdjobs.bdjobs.com/new_mybdjobs/step_01_view.asp'
edit_resume_link = driver.find_element(By.XPATH, f'//a[@href="{EDIT_RESUME_LINK}"]')
edit_resume_link.click()
time.sleep(3)

# Go to education tab
education_tab_link = driver.find_element(By.XPATH, '//button[@class="btn btn-tab-education"]')
education_tab_link.click()
time.sleep(3)

# Create new block for adding education
education_tab_link = driver.find_element(By.XPATH, '//button[@id="btnAdd_aca"]')
education_tab_link.click()
time.sleep(3)

# creating soup from page source
soup = BeautifulSoup(driver.page_source, 'html.parser')

with open("source.html", "w+", encoding="utf-8") as file:
    file.write(soup.prettify())
