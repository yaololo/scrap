from selenium import webdriver
from bs4 import BeautifulSoup
import getpass
import requests
from selenium.webdriver.common.keys import Keys
import pprint
userid = "yong_ming@live.com"
password = "changshou"
chrome_path = './chromedriver'
driver = webdriver.Chrome(chrome_path)
driver.get("https://www.linkedin.com")
driver.implicitly_wait(6)
driver.find_element_by_xpath("""//*[@id="session_key"]""").send_keys(userid)
driver.find_element_by_xpath("""//*[@id="session_password"]""").send_keys(password)
driver.find_element_by_class_name("sign-in-form__submit-button").click()

print("successfully login")

#  after login, visit google
googleLinkedInUrl = "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%221441%22%2C%2217876832%22%2C%22791962%22%2C%2216140%22%2C%2210440912%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH"
driver.get(googleLinkedInUrl)

ulCss = "search-results__list list-style-none "
element = driver.find_element_by_xpath("""//ul[contains(@class, 'search-results__list list-style-none ')]""")

all_li = element.find_elements_by_tag_name('li')
print(len(all_li))

for i in range(len(all_li)):
  # all_a = all_li[i].find_element_by_tag_name("a")
  # print(all_a.text)
  if i > 6:
    print(all_li[i].get_attribute("outerHTML"))
  # print(i, len(all_a))

# for idx, li in all_li:
#     all_a = li.find_elements_by_tag_name("a")
#     print(idx, len(all_a))
# #     for a in all_a:
# #       text = a.get_attribute('href')
# #       print(text)
