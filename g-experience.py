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
time.sleep(2)

driver.find_element_by_xpath("""//*[@id="session_key"]""").send_keys(userid)
driver.find_element_by_xpath(
    """//*[@id="session_password"]""").send_keys(password)
driver.find_element_by_class_name("sign-in-form__submit-button").click()

print("successfully login")

def get_top_block(top_block):
  uls = top_block.find_elements_by_tag_name("ul")
  name = uls[0].find_elements_by_tag_name("li")[0].text

  current_title = top_block.find_element_by_tag_name("h2").text

  # Third line block
  lis = uls[1].find_elements_by_tag_name("li")
  location = lis[0].text
  connections = lis[1].text

  return [name, current_title, location, connections]


def get_education(education_block):
  # Education blocks
  lis = education_block.find_elements_by_xpath("""ul/li""")
  school_names = []
  durations = []
  degree_names = []
  fields_of_study = []

  for li in lis:
    education_info = li.find_element_by_xpath("""div/div/a[@data-control-name='background_details_school']""")
    school_name = education_info.find_element_by_tag_name("h3").text
    school_names.append(school_name)

    duration = "na"
    with_duration = education_info.find_elements_by_xpath("""div//p[contains(@class, 'pv-entity__dates t-14 t-black--light t-normal')]""")
    if len(with_duration) > 0:
      duration = with_duration[0].find_elements_by_tag_name("span")[1].text.replace("–", "-")

    durations.append(duration)

    degree_name = "na"
    field_of_study = "na"
    with_degree = education_info.find_element_by_xpath("""div//div""").find_elements_by_tag_name("p")
    if len(with_degree) > 0:
      degree_name = with_degree[0].find_elements_by_tag_name("span")[1].text
      if len(with_degree) > 1:
        field_of_study = with_degree[1].find_elements_by_tag_name("span")[1].text

    degree_names.append(degree_name)
    fields_of_study.append(field_of_study)

  return ["|".join(school_names), "|".join(durations), "|".join(degree_names), "|".join(fields_of_study)]

def get_experience(url):
  #  visit url
  driver.get(url)

  # Scroll page down to bottom to load all DOM element
  driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });")
  time.sleep(2)

  # Click to expand industrial skills section
  click_button_script = "var buttons = document.getElementsByClassName('pv-profile-section__card-action-bar pv-skills-section__additional-skills artdeco-container-card-action-bar artdeco-button artdeco-button--tertiary artdeco-button--3 artdeco-button--fluid'); if(buttons.length>0) {buttons[0].click()}"

  driver.execute_script(click_button_script)
  time.sleep(1)

  print("after click on button")

  row = [url]
  main_element = driver.find_element_by_xpath("""//main[contains(@class, 'core-rail')]""")

  top_block = main_element.find_element_by_xpath("""div//section[contains(@class, 'pv-top-card artdeco-card ember-view')]//div[contains(@class, 'flex-1 mr5')]""")
  top_block_information = get_top_block(top_block)

  # Add top information to list
  row += top_block_information


  education_section = main_element.find_elements_by_xpath("""//section[@id="education-section"]""")

  # if no education block, put na for school_name, durations, degree_names, and fields_of_study
  education_information = ["na", "na", "na", "na"]
  if len(education_section) > 0:
    education_information =get_education(education_section[0])

  # Add education information to list
  row += education_information


  skill_blocks = main_element.find_elements_by_xpath("""//div[@id="skill-categories-expanded"]/div//ol/li//span[contains(@class, 'pv-skill-category-entity__name-text t-16 t-black t-bold')]""")
  skills = []
  for skill in skill_blocks:
    skills.append(skill.text)


  # Add education information to list
  row.append( "|".join(skills))

  print(row)
  return row

def write_employee_experience(index):
    with open(f'./google/employee_file{index}.csv', encoding='utf-8-sig') as csv_file_open:
        csv_reader = csv.reader(csv_file_open, delimiter=',')

        with open(f"./employee_experience/employee_experience{index}.csv", mode='w', newline='', encoding='utf-8-sig') as csv_file_write:
            fieldnames = ['employee_url','name','current_job_title', "current_location", "connections", "schools", "durations", "degree_name", "field_of_study", "industrial_skills"]
            writer = csv.writer(csv_file_write, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(fieldnames)

            count = 0
            for row in csv_reader:
                if count > 0:
                    print("user_link: ", row[0])
                    employee_experience = get_experience(row[0])
                    writer.writerow(employee_experience)
                    print("================== write user completed ===================")

                count += 1

    print("================== write file completed ===================")


# get_experience("file:///C:/Users/yongming/side_project/scrap/uni-code.html")
# get_experience("file:///C:/Users/yongming/side_project/scrap/test.html")
# get_experience("https://www.linkedin.com/in/raunak-bhandari/")

# for i in range(50):
#     if i > 5:
#         write_employee_experience(i+1)
write_employee_experience(1)
