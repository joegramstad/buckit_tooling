import csv

filename = "final_2.csv"
filename2 = "plot_cleaned.csv"
new_rows_list = []

with open(filename, 'r', encoding='cp1252') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        id = row[0]
        plot = row[1]

        new_row = [id, plot]
        print(new_row)
        new_rows_list.append(new_row)


file2 = open(filename2, 'w', encoding='utf-8', newline='')
writer = csv.writer(file2)
writer.writerows(new_rows_list)
file2.close()