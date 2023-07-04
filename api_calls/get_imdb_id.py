import csv
import requests

ERROR = "n/a"
ENCODING = "encoding error"

url = 'https://www.omdbapi.com/?apikey='
api_key = '789c5544'
title_param = '&t='
year_param = '&y='
id_param = '&i='

filename = "titles.csv"
filename2 = "titled.csv"

title = None
year = None

new_rows_list = []

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        id = row[0]
        id = id.strip()
        full_req = url + api_key + id_param + id

        # year = row[0]
        # title = row[1]
        # year = year.strip()
        # title = title.strip()
        # adj_title = title.replace(" ", "+")

        # year_under = str(int(year) - 1)
        # year_over = str(int(year) + 1)
        #
        # full_req_under = url + api_key + title_param + adj_title + year_param + year_under
        # full_req_over = url + api_key + title_param + adj_title + year_param + year_over


        r = requests.get(url=full_req)
        try:
            data = r.json()
            if data['Response'] == "True":
                title = data['Title']
                year = data['Year']
                # id_under = data['imdbID']
                # year_under = data['Year']
            else:
                year = ERROR
                title = ERROR
        except ValueError:
            title = ENCODING
            year = ENCODING
            print("decoding error")


        # r = requests.get(url=full_req_over)
        # try:
        #     data = r.json()
        #     if data['Response'] == "True":
        #         id_over = data['imdbID']
        #         year_over = data['Year']
        #     else:
        #         id_over = ERROR
        #         year_over = ERROR
        # except ValueError:
        #     id_over = ENCODING
        #     year_over = ENCODING
        #     print("decoding error")


        # new_row = [year, title, id_under, year_under, id_over, year_over]
        new_row = [id, title, year]
        print(new_row)
        new_rows_list.append(new_row)

file2 = open(filename2, 'w', newline='')
writer = csv.writer(file2)
writer.writerows(new_rows_list)
file2.close()
