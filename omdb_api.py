import csv
import sys
import requests
# import csv_master

NOT_FOUND_ERROR = "not found error"
ENCODING_ERROR = "encoding error"
COMMAND_NOT_FOUND_MSG = "Command not found. Please enter 'help' for list of commands"

URL = 'https://www.omdbapi.com/?apikey='
API_KEY = '789c5544'
TITLE_PARAM = '&t='
YEAR_PARAM = '&y='
ID_PARAM = '&i='
PLOT_PARAM = '&plot='

commands = {
    "help",
    "get imdb id",
    "get movie info"
}


def help_commands():
    print(commands)


def get_imdb_id(input_filename, output_filename):
    new_rows_list = []
    new_rows_list.append(["year", "title", "title_only_imdb_id", "title_only_title", "title_only_year", "both_imdb_id",
                          "both_title", "both_year", "minus1_only_imdb_id", "minus1_only_title", "minus1_only_year",
                          "plus1_imdb_id", "plus1_title", "plus1_only_year"])

    with open(input_filename, 'r', encoding='utf-8') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            year = row[0].strip()
            title = row[1].strip()

            new_row = [year, title]

            adj_title = title.replace(" ", "+")

            url_req = URL + API_KEY + TITLE_PARAM + adj_title

            for i in range(3):

                r = requests.get(url=url_req)
                r.encoding = 'utf-8'

                try:
                    data = r.json()
                    if data['Response'] == "True":
                        resp_imdb_id = data['imdbID']
                        resp_title = data['Title']
                        resp_year = data['Year']
                        print(title)
                    else:
                        resp_imdb_id = NOT_FOUND_ERROR
                        resp_title = NOT_FOUND_ERROR
                        resp_year = NOT_FOUND_ERROR

                except ValueError:
                    resp_imdb_id = ENCODING_ERROR
                    resp_title = ENCODING_ERROR
                    resp_year = ENCODING_ERROR

                except UnicodeDecodeError:
                    resp_imdb_id = ENCODING_ERROR
                    resp_title = ENCODING_ERROR
                    resp_year = ENCODING_ERROR

                new_row.append(resp_imdb_id)
                new_row.append(resp_title)
                new_row.append(resp_year)

                try:
                    if i < 2:
                        year = int(year) + (i * -1)
                    else:
                        year = int(year) + i

                except ValueError:
                    year = 2002

                url_req = URL + API_KEY + TITLE_PARAM + adj_title + YEAR_PARAM + str(year)

            new_rows_list.append(new_row)

    write_csv(new_rows_list, output_filename)


def get_movie_info(input_filename, output_filename, plot_size='full'):
    new_rows_list = []
    with open(input_filename, 'r', encoding='utf-8') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            imdb_id = row[0].strip()
            full_req = URL + API_KEY + ID_PARAM + imdb_id + PLOT_PARAM + plot_size

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
                    title = NOT_FOUND_ERROR
                    released = NOT_FOUND_ERROR
                    runtime = NOT_FOUND_ERROR
                    plot = NOT_FOUND_ERROR
                    country = NOT_FOUND_ERROR
                    language = NOT_FOUND_ERROR
                    poster = NOT_FOUND_ERROR

            except ValueError:
                title = ENCODING_ERROR
                released = ENCODING_ERROR
                runtime = ENCODING_ERROR
                plot = ENCODING_ERROR
                country = ENCODING_ERROR
                language = ENCODING_ERROR
                poster = ENCODING_ERROR

            new_row = [imdb_id, title, released, runtime, country, language, plot, poster]
            new_rows_list.append(new_row)


    write_csv(new_rows_list, output_filename)


def main(argv):
    input_file = argv[1]
    output_file = argv[2]

    while True:
        command = input("What would you like to do?: ")
        if command in commands:
            if command == "get movie info":
                command = input("What type of plot summary? (short or full): ")
                if command == 'short':
                    get_movie_info(input_file, output_file, 'short')
                else:
                    get_movie_info(input_file, output_file)
            elif command == "get imdb id":
                get_imdb_id(input_file, output_file)

        else:
            print(COMMAND_NOT_FOUND_MSG)
            continue

def write_csv(rows_list, output_filename, desired_encoding='utf8'):
    output_file = open(output_filename, 'w', newline='', encoding=desired_encoding)
    writer = csv.writer(output_file)
    writer.writerows(rows_list)
    output_file.close()

main(sys.argv)
