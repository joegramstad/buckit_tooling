import csv
import requests

ERROR = "n/a"
ENCODING = "encoding error"

url = 'https://www.omdbapi.com/?apikey='
api_key = '789c5544'
id_param = '&i='
plot_param = '&plot=full'

filename = "original.csv"
filename2 = "final.csv"

title = None
year = None

new_rows_list = []

with open(filename, 'r', encoding='utf-8') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        id = row[0]
        full_req = url + api_key + id_param + id + plot_param

        r = requests.get(url=full_req)
        r.encoding = 'utf-8'
        try:
            data = r.json()
            if data['Response'] == "True":
                title = data['Title']
                released = data['Released']
                runtime = data['Runtime']
                plot = data['Plot']
                country = data['Country']
                language = data['Language']
                poster = data['Poster']

            else:
                title = ERROR
                released = ERROR
                runtime = ERROR
                plot = ERROR
                country = ERROR
                language = ERROR
                poster = ERROR

        except ValueError:
            title = ENCODING
            released = ENCODING
            runtime = ENCODING
            plot = ENCODING
            country = ENCODING
            language = ENCODING
            poster = ENCODING

        new_row = [id, title, released, runtime, country, language, plot, poster]
        print(new_row)
        new_rows_list.append(new_row)

file2 = open(filename2, 'w', encoding='utf-8', newline='')
writer = csv.writer(file2)
writer.writerows(new_rows_list)
file2.close()
