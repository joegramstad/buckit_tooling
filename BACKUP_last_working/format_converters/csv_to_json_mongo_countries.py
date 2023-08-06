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


def get_entry_dict(row, sub_category=None):

    entry_dict = {
        'objectName': row[6].strip(),
        'objectID': row[7].strip(),
        'primaryContext': row[9].strip(),
        'secondaryContext': row[10].strip(),
    }

    if sub_category:
        entry_dict['subCategory'] = sub_category

    return entry_dict


def get_collection_dict(category_dict, entries, is_divided, types_dict):

    return {
        'collectionListCategory': category_dict['collectionListCategory'],
        'collectionListType': category_dict['collectionListType'],
        'collectionListOwner': category_dict['collectionListOwner'],
        'name': category_dict['name'],
        'isDivided': is_divided,
        'entries': entries,
        'types': types_dict
    }


def new_collection(row):
    category_dict = get_category_dict(row)

    sub_category = row[5].strip()

    if sub_category == "n/a":
        is_divided = False
        entry_dict = get_entry_dict(row)
    else:
        is_divided = True
        entry_dict = get_entry_dict(row, sub_category)

    entries = []
    entries.append(entry_dict)

    types_dict = get_types_dict(row)

    collection_entry = get_collection_dict(category_dict, entries, is_divided, types_dict)

    return collection_entry


def add_to_collection(row, cur_collection):
    sub_category = row[5].strip()

    entries = cur_collection['entries']

    if cur_collection['isDivided']:
        entry_dict = get_entry_dict(row, sub_category)

    else:
        entry_dict = get_entry_dict(row)

    entries.append(entry_dict)


def json_write(all_entries, output_file):
    json_object = json.dumps(all_entries, indent=4, ensure_ascii=False)

    with open(output_file, "w", encoding='utf-8') as outfile:
        outfile.write(json_object)


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
                collections.append(cur_collection)
                cur_hashed = hashed
                cur_collection = new_collection(row)

        collections.append(cur_collection)

    json_write(collections, output_file)


main(sys.argv)