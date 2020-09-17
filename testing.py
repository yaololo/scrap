import csv

with open('./google/employee_file1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
      if "profile_link" not in row[0]:
        print(row)
