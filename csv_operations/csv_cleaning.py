import csv
import utilities as util

with open('../test.csv', 'r', encoding='unicode_escape') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    master_list = []
    for row in csv_reader:
        new_row = ', '.join(row)
        new_row = new_row.strip()
        tokenized_row = new_row.split(", ")
        tokenized_row.sort()
        print(tokenized_row)
        tokenized_row = ', '.join(tokenized_row)
        master_list.append([tokenized_row])

    util.write_csv('cleaned', master_list)
