import json
import requests

url = 'https://www.omdbapi.com/?apikey='
api_key = '95915a61'
imdb_query = '&i=tt'
id_padding = '000000'

padding_len = 6
id_digits = 1
i = 1


while (True):
    if (len(str(i)) > id_digits):
        id_digits += 1
        padding_len -= 1
        id_padding = id_padding[0:padding_len]

    full_req = url + api_key + imdb_query + id_padding + str(i)
    r = requests.get(url=full_req)
    data = r.json()

    id = data['imdbID']
    title = data['Title']
    release_date = data['Released']
    minutes = data['Runtime'][:-4]
    metascore = data['Metascore']
    imdb = data['imdbRating']

    print("Movie: " + title + " released on: " + release_date + " with runtime of: " + minutes +
          " minutes. Has metacritic score: " + metascore + " and imdb score: " + imdb)

    i += 1





# full_req = 'https://www.omdbapi.com/?apikey=95915a61&i=tt0130010'






