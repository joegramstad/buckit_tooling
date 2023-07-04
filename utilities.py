import csv
import requests
from bs4 import BeautifulSoup
import re

PARENTHESES_ALL_TEXT = r'\([^)]*\)'
PARENTHESES_AND_SQ_BRACKETS = "[\(\[].*?[\)\]]"

def write_csv(csv_name, master_list, encoding='utf-8', newline=''):
    csv_name = csv_name + '.csv'
    with open(csv_name, 'a', encoding=encoding, newline=newline) as file:
        writer = csv.writer(file)
        writer.writerows(master_list)

def get_soup(url, parser='html.parser'):
    response = requests.get(url=url)
    return BeautifulSoup(response.content, parser)

def get_stripped_tag_text(component):
    return component.text.strip()

def remove_components_with_header(component, bad_header, tag='class'):
    return [x for x in component if bad_header not in x[tag]]

def soup_find_all_one_attr(soup, tag_name, attr_value, attr_name='class'):
    return soup.find_all(tag_name, attrs={attr_name: attr_value})

def soup_find_one_no_attr(soup, tag_name):
    return soup.find(tag_name)

def soup_find_all(soup, tag_name):
    return soup.find_all(tag_name)

def regex_replace_notes(text):
    return re.sub(PARENTHESES_AND_SQ_BRACKETS, '', text)

def print_all_tags(url, tag, attr_value=None):
    soup = get_soup(url)

    if attr_value:
        new_soup = soup_find_all_one_attr(soup, tag, attr_value)
    else:
        new_soup = soup_find_all(soup, tag)

    for elem in new_soup:
        print(elem)


