import utilities as util




# "Academy_Award_for_Best_Picture",
# "Academy_Award_for_Best_Director",
# "Academy_Award_for_Best_Actor",
# "Academy_Award_for_Best_Actress",
# "Academy_Award_for_Best_Cinematography",
# "Academy_Award_for_Best_Production_Design",
# "Academy_Award_for_Best_Adapted_Screenplay",
# "Academy_Award_for_Best_Sound",
# "Academy_Award_for_Best_Animated_Short_Film",
# "Academy_Award_for_Best_Live_Action_Short_Film",
# "Academy_Award_for_Best_Film_Editing",
# "Academy_Award_for_Best_Original_Score",
# "Academy_Award_for_Best_Original_Song",
# "Academy_Award_for_Best_Supporting_Actor",
# "Academy_Award_for_Best_Supporting_Actress",
# "Academy_Award_for_Best_Visual_Effects",
# "Academy_Award_for_Best_Original_Screenplay",
# "Academy_Award_for_Best_Documentary_Short_Film",
# "Academy_Award_for_Best_Documentary_Feature_Film",
# "List_of_Academy_Award_winners_and_nominees_for_Best_International_Feature_Film",
# "Academy_Award_for_Best_Costume_Design",
# "Academy_Award_for_Best_Makeup_and_Hairstyling",
# "Academy_Award_for_Best_Animated_Feature"
# 'BAFTA_Award_for_Best_Film',
# 'BAFTA_Award_for_Outstanding_British_Film',
# 'BAFTA_Award_for_Best_Film_Not_in_the_English_Language',
# 'BAFTA_Award_for_Best_Documentary',
# 'BAFTA_Award_for_Best_Animated_Film',
# 'BAFTA_Award_for_Best_Short_Film',
# 'BAFTA_Award_for_Best_Short_Animation',
# 'BAFTA_Award_for_Best_Direction',
# 'BAFTA_Award_for_Best_Adapted_Screenplay',
# 'BAFTA_Award_for_Best_Original_Screenplay',
# 'BAFTA_Award_for_Best_Actor_in_a_Leading_Role',
# 'BAFTA_Award_for_Best_Actress_in_a_Leading_Role',
# 'BAFTA_Award_for_Best_Actor_in_a_Supporting_Role',
# 'BAFTA_Award_for_Best_Actress_in_a_Supporting_Role',
# 'BAFTA_Award_for_Best_Cinematography',
# 'BAFTA_Award_for_Best_Editing',
# 'BAFTA_Award_for_Best_Costume_Design',
# 'BAFTA_Award_for_Best_Production_Design',
# 'BAFTA_Award_for_Best_Makeup_and_Hair',
# 'BAFTA_Award_for_Best_Original_Music',
# 'BAFTA_Award_for_Best_Sound',
# 'BAFTA_Award_for_Best_Special_Visual_Effects',
# 'BAFTA_Award_for_Best_Casting'
# 'Golden_Globe_Award_for_Best_Motion_Picture_–_Drama',
# 'Golden_Globe_Award_for_Best_Motion_Picture_–_Musical_or_Comedy',
# 'Golden_Globe_Award_for_Best_Foreign_Language_Film',
# 'Golden_Globe_Award_for_Best_Animated_Feature_Film',
# 'Golden_Globe_Award_for_Best_Director',
# 'Golden_Globe_Award_for_Best_Actor_–_Motion_Picture_Drama',
# 'Golden_Globe_Award_for_Best_Actor_–_Motion_Picture_Musical_or_Comedy',
# 'Golden_Globe_Award_for_Best_Actress_in_a_Motion_Picture_–_Drama',
# 'Golden_Globe_Award_for_Best_Actress_–_Motion_Picture_Comedy_or_Musical',
# 'Golden_Globe_Award_for_Best_Supporting_Actor_–_Motion_Picture',
# 'Golden_Globe_Award_for_Best_Supporting_Actress_–_Motion_Picture',
# 'Golden_Globe_Award_for_Best_Screenplay',
# 'Golden_Globe_Award_for_Best_Original_Score',
# 'Golden_Globe_Award_for_Best_Original_Song'
# 'Golden_Raspberry_Award_for_Worst_Picture',
# 'Golden_Raspberry_Award_for_Worst_Director',
# 'Golden_Raspberry_Award_for_Worst_Actor',
# 'Golden_Raspberry_Award_for_Worst_Actress',
# 'Golden_Raspberry_Award_for_Worst_Supporting_Actor',
# 'Golden_Raspberry_Award_for_Worst_Supporting_Actress'
# 'Golden_Lion',
# 'Grand_Jury_Prize_(Venice_Film_Festival)',
# 'Silver_Lion',
# 'Special_Jury_Prize_(Venice_Film_Festival)',
# 'Volpi_Cup_for_Best_Actor',
# 'Volpi_Cup_for_Best_Actress',
# 'Golden_Osella'


wiki_urls = [
'Hugo_Award_for_Best_Novel',
'Hugo_Award_for_Best_Novella',
'Hugo_Award_for_Best_Novelette',
'Hugo_Award_for_Best_Short_Story',
'Hugo_Award_for_Best_Series',
'Hugo_Award_for_Best_Related_Work',
'Hugo_Award_for_Best_Graphic_Story',
'Booker_Prize',
'Newbery_Medal',
'National_Book_Award_for_Nonfiction'
]


def main():
    for url in wiki_urls:
        print(url)
        scrape_wiki(url)


def clean_text(raw_text):
    clean_text = util.regex_replace_notes(raw_text)
    return clean_text.replace(",", "")


def scrape_wiki(path):

    master_list = [['BREAK', path]]

    url = "https://en.wikipedia.org/wiki/" + path

    soup = util.get_soup(url)
    tables = util.soup_find_all_one_attr(soup, 'table', 'wikitable')

    for table in tables:
        rows = util.soup_find_all(table, 'tr')

        placeholder = ""
        remaining_rows = 0

        for row in rows:
            winner = False
            short_list = []
            cols = util.soup_find_all(row, ['th', 'td'])

            if remaining_rows > 0:
                short_list.insert(0, placeholder)
                remaining_rows -= 1

            if cols:
                for col in cols:
                    entry = clean_text(col.text)

                    if entry and not entry.isspace():
                        short_list.append(entry)

                        if "rowspan" in col.attrs:
                            if row_count := col['rowspan']:
                                winner = True
                                remaining_rows = int(row_count) - 1
                                placeholder = entry

                if winner:
                    short_list.append("Winner")

            master_list.append(short_list)

    util.write_csv('lists_test', master_list)


main()