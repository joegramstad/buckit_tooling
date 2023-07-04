import csv

filename = 'stripee.csv'
filename2 = 'stripedfinal.csv'
new_rows_list = []

with open(filename, 'r', encoding="utf8") as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        try:
            original = row[0]
            original = original.strip()
        except:
            original = "ERROR"
            continue

        new_row = [original]
        print(new_row)
        new_rows_list.append(new_row)


file2 = open(filename2, 'w', newline='', encoding="utf8")
writer = csv.writer(file2)
writer.writerows(new_rows_list)
file2.close()