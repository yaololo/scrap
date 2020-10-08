from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
import pprint
import csv
import time

userid = "yong_ming@live.com"
password = "changshou"
chrome_path = './chromedriver'
driver = webdriver.Chrome(chrome_path)
driver.get("https://www.linkedin.com")
# driver.implicitly_wait(6)
time.sleep(6)

driver.find_element_by_xpath("""//*[@id="session_key"]""").send_keys(userid)
driver.find_element_by_xpath(
    """//*[@id="session_password"]""").send_keys(password)
driver.find_element_by_class_name("sign-in-form__submit-button").click()

print("successfully login")


def write_to_file(index):
    print(index)
    url = f"https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%221441%22%2C%2217876832%22%2C%22791962%22%2C%2216140%22%2C%2210440912%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH&page={index}"
    #  visit url
    print(url)
    time.sleep(1)

    driver.get(url)

    time.sleep(2)
    # Scroll page down to bottom to load all DOM element
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    element = driver.find_element_by_xpath(
        """//ul[contains(@class, 'search-results__list list-style-none ')]""")

    all_li = element.find_elements_by_tag_name('li')

    with open(f"./google/employee_file{index}.csv", mode='w') as csv_file:
        fieldnames = ['profile_link']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(all_li)):
            link = "" + \
                all_li[i].find_element_by_tag_name("a").get_attribute("href")

            # Filter out bot link
            if "search/results" not in link:
                writer.writerow({'profile_link': link})
                print(link)


for i in range(50):
    write_to_file(i+1)
