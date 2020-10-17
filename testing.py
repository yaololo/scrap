import csv

def get_data(index):
    with open(f"./format_employee_profile/employee_profile{index}.csv", mode='r', encoding='utf-8-sig', newline="") as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        writer = csv.writer(csv_file, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)

        rows = []
        for row in csv_reader:
            row[-1] = row[-1].split("        ")[0]
            rows.append(row)
            print(row)

    return rows


def writ_file(lst, index):
    with open(f"./format_employee_profile/employee_profile{index}.csv", mode='w', encoding='utf-8-sig', newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(lst)


for i in range(50):
    lst = get_data(i+1)
    writ_file(lst, i+1)


# data = [['American','美国人'],
#         ['Chinese','中国人']]

# with open(f"./new_google_employee_profile/employee_profile1.csv", mode='w', encoding='utf-8-sig') as f:
#     w = csv.writer(f)
#     w.writerows(data)
