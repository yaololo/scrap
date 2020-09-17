from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import getpass
import requests
from selenium.webdriver.common.keys import Keys
import pprint
import csv
import time

userid = "zhuangyongming1900@gmail.com"
password = "S9080047G@nus"
chrome_path = './chromedriver'
driver = webdriver.Chrome(chrome_path)
driver.get("https://www.linkedin.com")
driver.implicitly_wait(10)
# time.sleep(3)

# driver.find_element_by_xpath("""//*[@id="session_key"]""").send_keys(userid)
# driver.find_element_by_xpath(
#     """//*[@id="session_password"]""").send_keys(password)
# driver.find_element_by_class_name("sign-in-form__submit-button").click()

# print("successfully login")


def get_unique_job_titles(job_titles):
    empty_list = []
    for title in job_titles:
        print("*****")
        if "Company Name" not in title.text:
            print(title.text)


# def print_duration(durations):
#     for time in durations:
#         print(time.get_attribute())

def map_company_name(node):
    x = node.get_attribute("href").text.split("/")
    return x([len(x)-2]).replace("-", " ").title()


def get_employee_profile(url):

    #  visit url
    time.sleep(3)
    driver.get(url)
    time.sleep(2)

    # Scroll page down to bottom to load all DOM element
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    main_element = driver.find_element_by_xpath(
        """//main[contains(@class, 'core-rail')]""")

    # Get user name
    section_name = main_element.find_element_by_xpath(
        """//section[contains(@class, 'pv-top-card artdeco-card ember-view')]""")
    employee_name_li = section_name.find_element_by_xpath(
        """//li[contains(@class, 'inline t-24 t-black t-normal break-words')]""")
    employee_name = employee_name_li.text
    print(employee_name)

    # Get working experience
    section_working_experience = main_element.find_element_by_xpath(
        """//section[@id="experience-section"]""")
    all_work_experience_li = section_working_experience.find_elements_by_xpath(
        """//li[contains(@class, 'pv-entity__position-group-pager pv-profile-section__list-item ember-view')]""")
    # for work_li in all_work_experience_li:

    # duration h4.pv-entity__date-range t-14 t-black--light t-normal"
    durations = all_work_experience_li.find_elements_by_xpath(
        """//section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//h4[contains(@class, 'pv-entity__date-range t-14 t-black--light t-normal')]""")

    job_titles_same_company = all_work_experience_li.find_elements_by_xpath(
        """//section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//h3[contains(@class, 't-14 t-black t-bold')]//span""")

    unique_job_titles = all_work_experience_li.find_elements_by_xpath(
        """//section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//a//h3""")

    full_company_name = all_work_experience_li.find_elements_by_xpath(
        """//section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//a[@data-control-name='background_details_company']""")

    c_name = map(map_company_name, full_company_name)
    print("===========================================================================")

    for a in c_name:
        print(a)
    # compnay_name = section_working_experience.find_element_by_xpath(
    #     """//section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//a[@data-control-name='background_details_company']//p""")

    # print_duration(full_company_name)
    # get_unique_job_titles(unique_job_titles)
    # if len(company_header_h3_list) == 1:
    #   jobTitle = company_header_h3_list[0]

    # for a in company_header_h3_list:
    #   print("********")
    #   print(a.text)

# with open('./google/employee_file1.csv') as csv_file:
#   csv_reader = csv.reader(csv_file, delimiter=',')
#   count = 0
#   for row in csv_reader:
#     if count == 1:
#       print(row)
#       employee_profile = get_employee_profile(row[0])

#     count += 1


get_employee_profile("https://www.linkedin.com/in/doris-tang-22855461/")
