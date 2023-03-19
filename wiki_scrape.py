import sys
import utilities as util

WINNER = "Winner"
NOMINEE = "Nominee"

# works for oscars best acting awards(4) + best director
def scrape_wiki_actors(url, num_columns, start_year, award):
    master_list = []
    year = start_year - 1

    soup = util.get_soup(url)
    tables = util.soup_find_all_one_attr(soup, 'table', 'sortable')
    tables = util.remove_components_with_header(tables, 'plainrowheaders')

    remaining_rows = 0
    position = None
    insert_value = None

    for table in tables:
        rows = util.soup_find_all(table, 'tr')

        for row in rows:
            winners = []
            cells = util.soup_find_all(row, 'td')
            cur_index = 0

            for cell in cells:
                if cur_index >= num_columns:
                    year += 1
                    winners.append(WINNER)
                    continue
                if "rowspan" in cell.attrs:
                    remaining_rows = int(cell['rowspan'])
                    position = cur_index
                    insert_value = util.get_stripped_tag_text(cell)

                else:
                    winners.append(util.get_stripped_tag_text(cell))

                cur_index += 1

            if remaining_rows > 0:
                winners.insert(position, insert_value)
                remaining_rows -= 1

            winners.insert(0, year)
            if len(winners) > 1:
                master_list.append(winners)

    util.write_csv(award, master_list)

# works for pulitzer prize for fiction
def scrape_wiki_pulitzer(url):
    master_list = []

    soup = util.get_soup(url)
    tables = util.soup_find_all_one_attr(soup, 'table', 'sortable')

    for table in tables:
        rows = util.soup_find_all(table, 'tr')

        for row in rows:
            winner = []
            nominees_all = []
            cells = util.soup_find_all(row, 'td')
            cur_index = 0
            year = None

            for cell in cells:
                if cur_index == 0:
                    year = util.get_stripped_tag_text(cell)
                    winner.append(year)
                    winner.append(WINNER)
                elif cur_index < 3:
                    no_parentheses_txt = util.regex_replace_notes(util.get_stripped_tag_text(cell))
                    winner.append(no_parentheses_txt)
                elif cur_index == 6:
                    nominees = util.soup_find_all(cell, 'li')
                    for nominee in nominees:
                        nominee_name = util.get_stripped_tag_text(util.soup_find_one_no_attr(nominee, 'a'))
                        nominee_title = util.get_stripped_tag_text(util.soup_find_one_no_attr(nominee, 'i'))
                        nominees_all.append([year, NOMINEE, nominee_name, nominee_title])

                cur_index += 1

            master_list.append(winner)
            for nominee in nominees_all:
                master_list.append(nominee)

    util.write_csv('pulitzer', master_list)

def main(argv):
    award = argv[1]
    url = "https://en.wikipedia.org/wiki/" + award

    scrape_wiki_pulitzer(url)
    # num_columns = argv[2]
    # start_year = argv[3]
    # scrape_wiki_actors(url, int(num_columns), int(start_year), award)

# Pass in three args:
# 1. award (i.e. Academy_Award_for_Best_Actor)
# 2. number of columns in table (i.e. 3)
# 3. year of first award (i.e. 1928)
# full example: python wiki_scrape.py Academy_Award_for_Best_Actor 3 1928

main(sys.argv)
