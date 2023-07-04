import csv
import json
import sys


def get_category_dict(row):
    return {
        'collectionListCategory': row[0].strip(),
        'collectionListType': row[1].strip(),
        'collectionListOwner': row[2].strip(),
        'name': row[3].strip()
    }


def get_types_dict(row):
    return {
        'idType': row[11].strip(),
        'objectType': row[12].strip(),
        'primaryContextType': row[13].strip(),
        'secondaryContextType': row[14].strip()
    }


def get_entry_dict(row, status):
    if status == '1':
        winner = True
    else:
        winner = False

    entry_dict = {
        'objectName': row[6].strip(),
        'objectID': row[7].strip(),
        'winner': winner,
        'primaryContext': row[9].strip(),
        'secondaryContext': row[10].strip()
    }
    return entry_dict


def get_collection_dict(category_dict, year, entries, is_divided, types_dict):

    return {
        'collectionListCategory': category_dict['collectionListCategory'],
        'collectionListType': category_dict['collectionListType'],
        'collectionListOwner': category_dict['collectionListOwner'],
        'name': category_dict['name'],
        'year': year,
        'subCategories': is_divided,
        'entries': entries,
        'types': types_dict
    }


def new_collection(row):
    category_dict = get_category_dict(row)

    year = row[4].strip()
    sub_category = row[5].strip()
    status = row[8].strip()

    entry_dict = get_entry_dict(row, status)
    types_dict = get_types_dict(row)

    is_divided = False
    entries = {}
    if sub_category != "n/a":
        is_divided = True
        entries[sub_category] = []

    collection_entry = get_collection_dict(category_dict, year, entries, is_divided, types_dict)

    if is_divided:
        entries_array = collection_entry['entries'][sub_category]
    else:
        entries_dict = collection_entry['entries']
        entries_dict['ALL'] = []
        entries_array = entries_dict['ALL']

    entries_array.append(entry_dict)

    return collection_entry


def add_to_collection(row, cur_collection):
    sub_category = row[5].strip()
    status = row[8].strip()

    entries_dict = cur_collection['entries']

    if cur_collection['subCategories']:
        if sub_category not in entries_dict:
            entries_dict[sub_category] = []

        entries_array = entries_dict[sub_category]

    else:
        entries_array = entries_dict['ALL']

    entry_dict = get_entry_dict(row, status)
    entries_array.append(entry_dict)


def json_write(all_entries, output_file):
    json_object = json.dumps(all_entries, indent=4, ensure_ascii=False)

    # with open(output_file, "a", encoding='utf-8') as outfile:
    with open(output_file, "w", encoding='utf-8') as outfile:
        outfile.write(json_object)
        # outfile.write("\n")
        # outfile.write("\n")


def main(argv):
    filename = argv[1]
    input_file = filename + '.csv'
    output_file = filename + '.json'

    collections = []

    with open(input_file, 'r', encoding='utf-8') as csvfile:
        datareader = csv.reader(csvfile)

        next(datareader)
        first_row = next(datareader)

        cur_hashed = hash(first_row[15].strip())
        cur_collection = new_collection(first_row)

        for row in datareader:

            hashed = hash(row[15].strip())

            if hashed == cur_hashed:
                add_to_collection(row, cur_collection)

            else:
                # json_write(cur_collection, output_file)
                collections.append(cur_collection)
                cur_hashed = hashed
                cur_collection = new_collection(row)
        # json_write(cur_collection, output_file)
        collections.append(cur_collection)

    json_write(collections, output_file)


main(sys.argv)
