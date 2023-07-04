import json
import requests
import mysql.connector

# url = 'https://www.omdbapi.com/?apikey='
# api_key = '95915a61'
# imdb_query = '&i=tt'
# id_padding = '000000'
#
# padding_len = 6
# id_digits = 1
# i = 1


url = 'https://www.omdbapi.com/?apikey='
api_key = '789c5544'
imdb_query = '&i=tt'
id_padding = '0'

padding_len = 1
id_digits = 6
i = 168699


mydb = mysql.connector.connect(
    host="localhost",
    user="gramstad",
    password="joey91",
    database="buckit_movies"
)

my_cursor = mydb.cursor()
sql = "INSERT INTO movies (title, release_year, runtime_mins, metascore_rating, imdb_rating, imdb_id) VALUES (%s, %s, %s, %s, %s, %s)"

while (True):
    if (len(str(i)) > id_digits):
        id_digits += 1
        padding_len -= 1
        id_padding = id_padding[0:padding_len]

    full_req = url + api_key + imdb_query + id_padding + str(i)
    r = requests.get(url=full_req)
    data = r.json()

    if data['Response'] == "True":

        id = data['imdbID']
        title = data['Title']
        if (title == '#DUPE#'):
            i += 1
            continue


        year = data['Year']
        if (len(year) > 4):
            year = '0'


        if (data['Runtime'] != 'N/A'):
            minutes = data['Runtime'][:data['Runtime'].find(' ')]
            minutes = 1 if minutes[-1] == 'S' else minutes
        else:
            minutes = 0

        metascore = 0 if data['Metascore'] == 'N/A' else data['Metascore']
        imdb = 0 if data['imdbRating'] == 'N/A' else data['imdbRating']

        val = (title, year, minutes, metascore, imdb, id)

        print(val)

        my_cursor.execute(sql, val)

        mydb.commit()
        print(my_cursor.rowcount, "record inserted.")

        i += 1

    else:
        print(i, " Passed over.")
        i += 1
        continue
