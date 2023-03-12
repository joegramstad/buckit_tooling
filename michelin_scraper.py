import csv

import requests
from bs4 import BeautifulSoup

url = 'https://guide.michelin.com/us/en/restaurants/'

michelin_urls = {
    "3-stars-michelin": 7,
    "2-stars-michelin": 25,
    "1-star-michelin": 138,
    "bib-gourmand": 169,
    "sustainable_gastronomy": 22
}

for entry in michelin_urls.items():
    level = entry[0]
    pages = entry[1]
    request_url = url + level
    i = 1
    all_entries = []

    while i <= pages:

        response = requests.get(url=request_url)

        soup = BeautifulSoup(response.content, 'html.parser')
        restaurants = soup.find_all('div', attrs={"class": "card__menu-content"})

        for restaurant in restaurants:
            # michelin_award = restaurant.find('img', attrs={"class": "michelin-award"})
            # award_type = michelin_award['src']
            # right_index = award_type.rfind('.')
            # left_index = award_type.find('/')
            # award = award_type[left_index, right_index]

            restaurant_title = restaurant.find('h3', attrs={"class": "card__menu-content--title"})
            title = restaurant_title.text.strip()

            restaurant_location = restaurant.find('div', attrs={"class": "card__menu-footer--location"})
            location = restaurant_location.text.strip()

            restaurant_cuisine = restaurant.find('div', attrs={"class": "card__menu-footer--price"})
            cuisine_raw = restaurant_cuisine.text

            cuisine_index = cuisine_raw.rfind('·')
            if cuisine_index == -1:
                cuisine = cuisine_raw.strip()
            else:
                cuisine = cuisine_raw[cuisine_index + 1:]
                cuisine = cuisine.strip()


            entry = [level, location, title, cuisine]
            print(entry)
            all_entries.append(entry)

        i += 1

        if i == 2:
            request_url = request_url + '/page/'
        else:
            request_url = request_url[:request_url.rfind('/') + 1]

        request_url = request_url + str(i)

    with open('michelin.csv', 'a', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_entries)

    all_entries = []
