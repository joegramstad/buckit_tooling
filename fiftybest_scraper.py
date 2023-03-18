import sys
import utilities

START_YEAR = 2002
PREVIOUS_LISTS_URL = 'https://www.theworlds50best.com/previous-list/'
CURRENT_50_URL = "https://www.theworlds50best.com/list/1-50"


def main(argv):
    skip_years = set([2020])
    cur_year = int(argv[1])

    year = START_YEAR

    soup = utilities.get_soup(PREVIOUS_LISTS_URL + str(START_YEAR))
    restaurants = soup.find_all('div', attrs={"class": "item"})

    for restaurant in restaurants:
        rank = restaurant.find('p', attrs={"class": "position"})
        name = restaurant.find('h2')
        location = name.next_sibling

        results = [year, rank.text.strip(), name.text.strip(), location.text.strip()]
        print(results)

        if rank.text.strip() == "50":
            year += 1
            if year in skip_years:
                year += 1

    soup = utilities.get_soup(CURRENT_50_URL)

    cur_restaurants_first = soup.find_all('a', attrs={"class": "item"})
    cur_restaurants_second = soup.find_all('div', attrs={"class": "item"})
    cur_restaurants_first = cur_restaurants_first[:50]

    for restaurant in cur_restaurants_first:
        rank = restaurant.find('p', attrs={"class": "position"})
        name = restaurant.find('h2')
        location = name.next_sibling
        results = [cur_year, rank.text.strip(), name.text.strip(), location.text.strip()]
        print(results)

    for restaurant in cur_restaurants_second:
        rank = restaurant.find('p', attrs={"class": "position"})
        name = restaurant.find('h2')
        location = name.next_sibling
        results = [cur_year, rank.text.strip(), name.text.strip(), location.text.strip()]
        print(results)

main(sys.argv)
