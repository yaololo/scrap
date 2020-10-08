from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pprint
import csv
import time

userid = "bob90937@gmail.com"
password = "bob()(#&"
chrome_path = './chromedriver'
driver = webdriver.Chrome(chrome_path)
driver.get("https://www.linkedin.com")
time.sleep(3)

driver.find_element_by_xpath("""//*[@id="session_key"]""").send_keys(userid)
driver.find_element_by_xpath(
    """//*[@id="session_password"]""").send_keys(password)
driver.find_element_by_class_name("sign-in-form__submit-button").click()

print("successfully login")


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

    print(rows)
    return rows


def handle_unique_working_block(block, profile_url, name):
    row = []
    job_title = block.find_element_by_xpath(
        """h3[contains(@class, 't-16 t-black t-bold')]""").text

    company_info = block.find_element_by_xpath(
        """p[contains(@class, 'pv-entity__secondary-title t-14 t-black t-normal')]""")
    company_name = company_info.text

    # Remove Job types E.g Part-time, Full-time, Contract
    job_types = company_info.find_elements_by_tag_name("span")
    if len(job_types) > 0:
        script = "var nodes = arguments[0]; nodes.removeChild(nodes.childNodes[1]); return nodes.textContent.replaceAll('\\n', '').trim();"

        company_name = driver.execute_script(
            script, company_info)

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

    return row


def get_employee_profile(url):
    #  visit url
    time.sleep(3)
    driver.get(url)
    # driver.get("file:///Users/yozhuan/project/scraper/test.html")
    time.sleep(2)

    # Scroll page down to bottom to load all DOM element
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(1)

    main_element = driver.find_element_by_xpath(
        """//main[contains(@class, 'core-rail')]""")

    # Get user name
    section_name = main_element.find_element_by_xpath(
        """//section[contains(@class, 'pv-top-card artdeco-card ember-view')]""")
    employee_name_li = section_name.find_element_by_xpath(
        """//li[contains(@class, 'inline t-24 t-black t-normal break-words')]""")
    employee_name = employee_name_li.text

    # Get working experience blocks
    working_experience_block = main_element.find_elements_by_xpath(
        """//section[@id="experience-section"]//li[contains(@class, 'pv-entity__position-group-pager pv-profile-section__list-item ember-view')]""")
    group_working_exp = []

    # Consolidate data in each working experience block
    for working_li in working_experience_block:
        same_c_lis = working_li.find_elements_by_xpath(
            """section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//ul//li""")

        # Check if there is multiple working experience within in the same company
        if len(same_c_lis) > 0:
            company_name = working_li.find_element_by_xpath(
                """section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//div[contains(@class, 'pv-entity__company-summary-info')]//h3[contains(@class, 't-16 t-black t-bold')]""").find_elements_by_tag_name("span")[1].text

            group_working_exp += handle_same_company(
                same_c_lis, company_name, url, employee_name)

        else:
            unique_working_block = working_li.find_element_by_xpath(
                """section[contains(@class, 'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')]//a[@data-control-name='background_details_company']//div[contains(@class, 'pv-entity__summary-info pv-entity__summary-info--background-section mb2')]""")
            group_working_exp.append(
                handle_unique_working_block(unique_working_block, url, employee_name))

    print(group_working_exp)

    return group_working_exp


get_employee_profile("https://www.linkedin.com/in/yilin-chiam-aa376886/")
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
