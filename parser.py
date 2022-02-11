import time

from bs4 import BeautifulSoup
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import xlsxwriter

from helpers import get_search_strings

SIGN_IN_PAGE = 'https://mybdjobs.bdjobs.com/mybdjobs/signin.asp'
USERNAME = config('USERNAME')
PASSWORD = config('PASSWORD')

driver = webdriver.Chrome('chromedriver.exe')

# Getting log in page
driver.get(SIGN_IN_PAGE)
time.sleep(5)

# Closing ad modal
close_modal_button = driver.find_element(
    By.XPATH,
    '//div[@class="modal-content"]/a'
)
close_modal_button.click()

# Fill up username
username_field = driver.find_element(By.ID, 'TXTUSERNAME')
sign_in_next_button = driver.find_element(
    By.XPATH,
    '//input[@class="btn btn-success btn-signin"]'
)
username_field.send_keys(USERNAME)
sign_in_next_button.click()
time.sleep(3)

# Fill up password
password_field = driver.find_element(By.ID, 'TXTPASS')
sign_in_complete_button = driver.find_element(
    By.XPATH,
    '//input[@class="btn btn-success btn-signin"]'
)
password_field.send_keys(PASSWORD)
sign_in_complete_button.click()
time.sleep(3)

# Go to Edit resume page
EDIT_RESUME_LINK = 'https://mybdjobs.bdjobs.com/new_mybdjobs/step_01_view.asp'
edit_resume_link = driver.find_element(
    By.XPATH,
    f'//a[@href="{EDIT_RESUME_LINK}"]'
)
edit_resume_link.click()
time.sleep(3)

# Go to education tab
education_tab_link = driver.find_element(
    By.XPATH,
    '//button[@class="btn btn-tab-education"]'
)
education_tab_link.click()
time.sleep(3)

# Create new block for adding education
education_create_button = driver.find_element(
    By.XPATH,
    '//button[@id="btnAdd_aca"]'
)
education_create_button.click()
time.sleep(5)

level_of_education_select = Select(driver.find_element(By.ID, 'cboEduLevel'))


def get_exams(level_id: str):
    global driver
    global level_of_education_select
    level_of_education_select.select_by_value(level_id)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    exam_element = [
        opt.text.strip() for opt in
        soup.find(id='txtExamTitle').find_all('option')
    ]
    return exam_element


# Getting SSC exams
psc_exams = get_exams('-3')
jsc_exams = get_exams('-2')
ssc_exams = get_exams('1')
hsc_exams = get_exams('2')
diploma_exams = get_exams('3')
bachelor_exams = get_exams('4')
masters_exams = get_exams('5')

# Getting concentration/major list
major = []
major_input = driver.find_element(By.ID, 'txtMajorGroup')
search_strings = get_search_strings()

for s in search_strings:
    major_input.clear()
    major_input.send_keys(s)
    major_input.click()
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    li_elements = soup.find(id='ui-id-1').find_all('li')
    if li_elements:
        for li in li_elements:
            print(li.find('a').text.strip())
            major.append(li.find('a').text.strip())
major = list(set(major))

# Getting institutions list
institution_input = driver.find_element(By.ID, 'txtInstituteName')
ids_for_institutions = ['1', '2', '3', '4']

# Configuring worksheet for writing xlsx file
column = 0
workbook = xlsxwriter.Workbook('1.xlsx')
worksheet = workbook.add_worksheet()

for level_id in ids_for_institutions:
    row = 0
    institutions = []
    level_of_education_select.select_by_value(level_id)

    for s in search_strings:
        institution_input.clear()
        institution_input.send_keys(s)
        institution_input.click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        li_elements = soup.find(id='ui-id-1').find_all('li')
        if li_elements:
            for li in li_elements:
                print(li.find('a').text.strip())
                institutions.append(li.find('a').text.strip())

    institutions = list(set(institutions))

    for ins in institutions:
        worksheet.write(row, column, ins)
        row += 1

    column += 1

workbook.close()
