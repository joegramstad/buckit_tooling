import csv
import requests

ERROR = "n/a"

url = 'https://www.omdbapi.com/?apikey='
api_key = '789c5544'
title_param = '&t='
year_param = '&y='

filename = "test.csv"
filename2 = "test_new.csv"

title = None
year = None

new_rows_list = []

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        year = row[0]
        title = row[1]
        adj_title = title.replace(" ", "+")

        full_req = url + api_key + title_param + adj_title + year_param + year
        print(full_req)
        r = requests.get(url=full_req)
        data = r.json()

        if data['Response'] == "True":
            id = data['imdbID']
        else:
            id = ERROR

        new_row = [id, title, year]
        print(new_row)
        new_rows_list.append(new_row)

file2 = open(filename2, 'w', newline='')
writer = csv.writer(file2)
writer.writerows(new_rows_list)
file2.close()
