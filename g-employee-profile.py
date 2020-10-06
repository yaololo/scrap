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

userid = "bob90937@gmail.com"
password = "bob()(#&"
chrome_path = './chromedriver'
driver = webdriver.Chrome(chrome_path)
driver.get("https://www.linkedin.com")
# driver.implicitly_wait(10)
time.sleep(3)

driver.find_element_by_xpath("""//*[@id="session_key"]""").send_keys(userid)
driver.find_element_by_xpath(
    """//*[@id="session_password"]""").send_keys(password)
driver.find_element_by_class_name("sign-in-form__submit-button").click()

print("successfully login")


def map_company_name(url):
    x = url.split("/")
    return x[len(x)-2].replace("-", " ").title()


def get_group_experience_list(groups):
    l = []
    for group in groups:
        x = group.find_elements_by_tag_name('li')
        for i in x:
            print(i.text)
        l.append(len(x))

    return l


def format_duration(durations):
    l = []
    for duration in durations:
        text = duration.find_elements_by_tag_name(
            "span")[1].text.replace("–", "-")
        l.append(text)

    return l


def get_all_data(employee_name, durations, company_url, unique_job_titles, job_titles_same_company, work_group_block):
    company_idx = 0
    unique_job_idx = 0
    job_title_idx = 0

    w_g_block_idx = 0
    curr_w_g_block_value = 0
    w_g_block_len = len(work_group_block)

    row = []
    if w_g_block_len == 0:
        for i in range(len(durations)):
            col = []
            c_url = company_url[i].get_attribute("href")
            col.append(employee_name)
            col.append(durations[i])
            col.append(unique_job_titles[i].text)
            col.append(c_url)
            col.append(map_company_name(c_url))
            row.append(col)

        return row
    else:
        curr_w_g_block_value = work_group_block[w_g_block_idx]

        for i in range(len(durations)):
            col = []
            print("================")
            col.append(employee_name)
            col.append(durations[i])

            if "Company Name" in unique_job_titles[unique_job_idx].text:
                if (curr_w_g_block_value > 0) and (curr_w_g_block_value - 1) == 0:
                    col.append(
                        job_titles_same_company[job_title_idx].text.split('\n')[1])
                    col.append(company_url[company_idx].get_attribute("href"))
                    col.append(map_company_name(
                        company_url[company_idx].get_attribute("href")))

                    unique_job_idx += 1
                    company_idx += 1
                    job_title_idx += 1
                    w_g_block_idx += 1

                    row.append(col)
                    if w_g_block_idx < w_g_block_len:
                        curr_w_g_block_value = work_group_block[w_g_block_idx]

                else:
                    col.append(
                        job_titles_same_company[job_title_idx].text.split('\n')[1])
                    col.append(company_url[company_idx].get_attribute("href"))
                    col.append(map_company_name(
                        company_url[company_idx].get_attribute("href")))

                    row.append(col)
                    curr_w_g_block_value -= 1
                    job_title_idx += 1
            else:
                col.append(unique_job_titles[unique_job_idx].text)
                col.append(company_url[company_idx].get_attribute("href"))
                col.append(map_company_name(
                    company_url[company_idx].get_attribute("href")))

                row.append(col)
                unique_job_idx += 1
                company_idx += 1
        return row


def handle_same_company(lis, company_name, profile_url, name):
    rows = []
    for li in lis:
        cols = []
        print("===============same company=================")
        job_title = li.find_element_by_xpath(
            """div[contains(@class, 'ember-view')]//h3[contains(@class, 't-14 t-black t-bold')]""").find_elements_by_tag_name("span")[1].text

        duration = li.find_element_by_xpath(
            """div[contains(@class, 'ember-view')]//h4[contains(@class, 'pv-entity__date-range t-14 t-black--light t-normal')]""").find_elements_by_tag_name("span")[1].text

        locations = li.find_elements_by_xpath(
            """div[contains(@class, 'ember-view')]//h4[contains(@class, 'pv-entity__location t-14 t-black--light t-normal block')]""")

        location = ""
        if len(locations) > 0:
            location = locations[0].find_elements_by_tag_name("span")[1].text

        cols.append(profile_url)
        cols.append(name)
        cols.append(duration)
        cols.append(location)
        cols.append(job_title)
        cols.append(company_name)
        rows.append(cols)

        print(company_name, job_title, duration, location)

    return rows


def handle_unique_working_block(block, profile_url, name):
    row = []
    job_title = block.find_element_by_xpath(
        """h3[contains(@class, 't-16 t-black t-bold')]""").text

    company_info = block.find_element_by_xpath(
        """p[contains(@class, 'pv-entity__secondary-title t-14 t-black t-normal')]""")
    company_name = company_info.text

    job_types = company_info.find_elements_by_tag_name("span")
    job_type = ""

    if len(job_types) > 0:
        job_type = job_types[0].text
        company_name = company_name.replace(job_type, "").strip()

    duration = block.find_element_by_xpath(
        """div[contains(@class, 'display-flex')]//h4[contains(@class, 'pv-entity__date-range t-14 t-black--light t-normal')]""").find_elements_by_tag_name("span")[1].text

    locations = block.find_elements_by_xpath(
        """h4[contains(@class, 'pv-entity__location t-14 t-black--light t-normal block')]""")

    location = ""
    if len(locations) > 0:
        location = locations[0].find_elements_by_tag_name("span")[1].text

    row.append(profile_url)
    row.append(name)
    row.append(duration)
    row.append(location)
    row.append(job_title)
    row.append(company_name)

    print(company_name, job_title, duration, location)
    return row


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
    # print(employee_name)

    # Get working experience
    # section_working_experience = main_element.find_element_by_xpath(
    #     """//section[@id="experience-section"]""")

    working_experience_block = main_element.find_elements_by_xpath(
        """//section[@id="experience-section"]//li[contains(@class, 'pv-entity__position-group-pager pv-profile-section__list-item ember-view')]""")

    print(len(working_experience_block))
    for working_li in working_experience_block:
        same_c_lis = working_li.find_elements_by_xpath(
            """section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//ul//li""")

        group_working_exp = []

        if len(same_c_lis) > 0:
            company_name = working_li.find_element_by_xpath(
                """section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//div[contains(@class, 'pv-entity__company-summary-info')]//h3[contains(@class, 't-16 t-black t-bold')]""").find_elements_by_tag_name("span")[1].text

            print("in group")
            group_working_exp = group_working_exp + \
                handle_same_company(
                    same_c_lis, company_name, url, employee_name)
        else:
            print("in individual")

            unique_working_block = working_li.find_element_by_xpath(
                """section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//a[@data-control-name='background_details_company']//div[contains(@class, 'pv-entity__summary-info pv-entity__summary-info--background-section mb2')]""")
            print("================================")
            group_working_exp.append(
                handle_unique_working_block(unique_working_block, url, employee_name))

    print(group_working_exp)

    return group_working_exp

    # group_working_experience = section_working_experience.find_elements_by_xpath(
    #     """//section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//ul[contains(@class, 'pv-entity__position-group mt2')]""")

    # g_working_block = get_group_experience_list(group_working_experience)

    # durations = section_working_experience.find_elements_by_xpath(
    #     """//section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//h4[contains(@class, 'pv-entity__date-range t-14 t-black--light t-normal')]""")

    # job_titles_same_company = section_working_experience.find_elements_by_xpath(
    #     """//section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//h3[contains(@class, 't-14 t-black t-bold')]""")

    # unique_job_titles = section_working_experience.find_elements_by_xpath(
    #     """//section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//a//h3""")

    # full_company_name = section_working_experience.find_elements_by_xpath(
    #     """//section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//a[@data-control-name='background_details_company']""")

    # formated_durations = format_duration(durations)

    # return get_all_data(employee_name, formated_durations, full_company_name,
    #                     unique_job_titles, job_titles_same_company, g_working_block)


get_employee_profile("https://www.linkedin.com/in/haliyusof/")
# a = get_employee_profile("https://www.linkedin.com/in/haliyusof/")
# print(a)


# def write_employee_profile(index):
#     print(index)
#     with open(f'./google/employee_file{index}.csv') as csv_file_open:
#         csv_reader = csv.reader(csv_file_open, delimiter=',')

#         with open(f"./google_employee_profile/employee_profile{index}.csv", mode='w') as csv_file_write:
#             fieldnames = ['name', 'duration', "job_title",
#                           "linkedIn_company_url", "company_name"]
#             writer = csv.writer(csv_file_write, delimiter=',',
#                                 quotechar='"', quoting=csv.QUOTE_MINIMAL)

#             writer.writerow(fieldnames)

#             count = 0
#             for row in csv_reader:
#                 if count > 0:
#                     print("user_link: ", row[0])
#                     employee_profile = get_employee_profile(row[0])
#                     for profile in employee_profile:
#                         writer.writerow(profile)
#                         print(profile)
#                         time.sleep(1)

#                     print("================== write user completed ===================")

#                 count += 1

#     print("================== write file completed ===================")


# for i in range(50):
#     write_employee_profile(i+1)