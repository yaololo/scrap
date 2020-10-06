# import csv

# with open(f"./google_employee_profile/employee_profile.csv", mode='w') as csv_file:
#     fieldnames = ['name', 'duration', "job_title",
#                   "company_url", "company_name"]
#     writer = csv.writer(csv_file, delimiter=',',
#                         quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     writer.writerow(fieldnames)

#     writer.writerow(['ss', 'sss', 'ssss', 'ddddd', 'ssdfa', 'sdfsdf'])
#     # for profile in employee_profile:
#     #     writer.writerow(profile)
#     #     print(profile)

a = "Airport Group Full-time"
b = "Full-time"

print(a.replace(b, ""))
