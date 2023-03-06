import sys
import requests
from bs4 import BeautifulSoup


CONFIGURATION = {
    "Actor": {

    }



}



def scrape_wiki_article(url, num_columns, start_year):
    response = requests.get(
        url=url,
    )

    year = start_year - 1

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', attrs={"class": "sortable"})

    remaining_rows = 0
    position = None
    insert_value = None

    tables = [x for x in tables if 'plainrowheaders' not in x['class'] ]

    for table in tables:
        data_rows = table.find_all('tr')

        for row in data_rows:
            winners = []
            data_elems = row.find_all('td')
            cur_index = 0

            for elem in data_elems:
                if cur_index >= num_columns:
                    year += 1
                    winners.append("Winner")
                    continue
                if "rowspan" in elem.attrs:
                    remaining_rows = int(elem['rowspan'])
                    position = cur_index
                    insert_value = elem.text.strip()

                else:
                    winners.append(elem.text.strip())

                cur_index += 1

            if remaining_rows > 0:
                winners.insert(position, insert_value)
                remaining_rows -= 1

            winners.insert(0, year)
            print(winners)


def main(argv):
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_" + argv[1]
    num_columns = argv[2]
    start_year = argv[3]
    scrape_wiki_article(url, int(num_columns), int(start_year))

# Pass in three args:
# 1. award (i.e. Actor)
# 2. number of columns in table (i.e. 3)
# 3. year of first award (i.e. 1928)
# full example: python wiki_scrape.py Actor 3 1928

main(sys.argv)
