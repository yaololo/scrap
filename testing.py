# import unicodecsv as csv

# data = [['American','美国人'],
#         ['Chinese','中国人']]

# with open(f"./google_employee_profile/employee_profile.csv", mode='w', encoding='utf-8') as csv_file:
#     csv_file.write('\ufeff'.encode('utf8'))

#     fieldnames = ['name', 'duration', "job_title",
#                   "company_url", "company_name"]
#     writer = csv.writer(csv_file, delimiter=',')
#     writer.writerow(fieldnames)

#     for row in data:
#        writer.writerow([item.encode('utf8') for item in row])

    # writer.writerow(s.encode('utf-8'), for s in ['ss', 'sss', 'ssss', 'ddddd', 'ssdfa', '兴中会'])
    # for profile in employee_profile:
    #     writer.writerow(profile)
    #     print(profile)

# a = "Airport Group Full-time"
# b = "Full-time"

# print(a.replace(b, ""))

import csv

data = [['American','美国人'],
        ['Chinese','中国人']]

with open(f"./google_employee_profile/employee_profile.csv", mode='w', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerows(data)
