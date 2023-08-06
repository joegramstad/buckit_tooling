import csv
import json
import sys

ERROR_MSG = "ERROR"
COMMAND_NOT_FOUND_MSG = "Command not found. Please enter 'help' for list of commands"

commands = {
    "help",
    "dynamo",
    "mongo"
}


def help_commands():
    print(commands)


def get_category_dict(row, json_type):
    if json_type == 'dynamo':
        return {
            'collectionListCategory': {
                "S": row[0].strip()
            },
            'collectionListType': {
                "S": row[1].strip()
            },
            'collectionListOwner': {
                "S": row[2].strip()
            },
            'name': {
                "S": row[3].strip()
            }
        }

    else:
        return {
            'collectionListCategory': row[0].strip(),
            'collectionListType': row[1].strip(),
            'collectionListOwner': row[2].strip(),
            'name': row[3].strip()
        }


def get_types_dict(row, json_type):
    if json_type == 'dynamo':
        return {
            'idType': {
                "S": row[11].strip()
            },
            'objectType': {
                "S": row[12].strip()
            },
            'primaryContextType': {
                "S": row[13].strip()
            },
            'secondaryContextType': {
                "S": row[14].strip()
            }
        }

    else:
        return {
            'idType': row[11].strip(),
            'objectType': row[12].strip(),
            'primaryContextType': row[13].strip(),
            'secondaryContextType': row[14].strip()
        }


def get_entry_dict_dynamo(row, sub_category):
    return {
        "M": {
            'sub_category': {
                "S": sub_category
            },
            'objectName': {
                "S": row[6].strip()
            },
            'primaryContext': {
                "S": row[9].strip()
            },
            'secondaryContext': {
                "S": row[10].strip()
            }
        }
    }


def get_entry_dict(row, status):
    if status == '1':
        winner = True
    else:
        winner = False

    return {
        'objectName': row[6].strip(),
        'objectID': row[7].strip(),
        'winner': winner,
        'primaryContext': row[9].strip(),
        'secondaryContext': row[10].strip()
    }


def get_collection_dict_dynamo(category_dict, types_dict, year, hashed):
    hashed = str(hashed)
    return {
        "Item": {
            'hash': {
                "N": hashed
            },
            'categories': {
                "M": category_dict
            },
            'year': {
                "N": year
            },
            'entries': {
                "M": {
                    'winner': {
                        "M": {

                        }
                    },
                    'nominee': {
                        "M": {

                        }
                    }
                }
            },
            'types': {
                "M": types_dict
            }
        }
    }


def get_collection_dict(category_dict, types_dict, year, entries, is_divided):
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


def new_collection(row, json_type, hashed=None):
    # SHARED
    year = row[4].strip()
    sub_category = row[5].strip()
    status = row[8].strip()

    if json_type == 'dynamo':
        category_dict = get_category_dict(row, 'dynamo')

        object_id = row[7].strip()

        entry_dict = get_entry_dict_dynamo(row, sub_category)
        types_dict = get_types_dict(row, 'dynamo')

        collection_entry = get_collection_dict_dynamo(category_dict, types_dict, year, hashed)

        if status == '1':
            edit_dict = collection_entry['Item']['entries']['M']['winner']['M']

        else:
            edit_dict = collection_entry['Item']['entries']['M']['nominee']['M']

        edit_dict[object_id] = entry_dict
        return collection_entry

    else:
        category_dict = get_category_dict(row, 'mongo')
        entry_dict = get_entry_dict(row, status)
        types_dict = get_types_dict(row, 'mongo')

        is_divided = False
        entries = {}
        if sub_category != "n/a":
            is_divided = True
            entries[sub_category] = []

        collection_entry = get_collection_dict(category_dict, types_dict, year, entries, is_divided)

        if is_divided:
            entries_array = collection_entry['entries'][sub_category]
        else:
            entries_dict = collection_entry['entries']
            entries_dict['ALL'] = []
            entries_array = entries_dict['ALL']

        entries_array.append(entry_dict)
        return collection_entry


def add_to_collection(row, cur_collection, json_type):
    # SHARED
    sub_category = row[5].strip()
    status = row[8].strip()

    if json_type == 'dynamo':
        collection_dict = cur_collection['Item']['entries']['M']
        object_id = row[7].strip()

        if status == '1':
            edit_dict = collection_dict['winner']['M']
        else:
            edit_dict = collection_dict['nominee']['M']

        entry_dict = get_entry_dict_dynamo(row, sub_category)

        edit_dict[object_id] = entry_dict

    else:
        entries_dict = cur_collection['entries']

        if cur_collection['subCategories']:
            if sub_category not in entries_dict:
                entries_dict[sub_category] = []

            entries_array = entries_dict[sub_category]

        else:
            entries_array = entries_dict['ALL']

        entry_dict = get_entry_dict(row, status)
        entries_array.append(entry_dict)


def json_write(rows_list, output_filename, json_type):
    json_object = json.dumps(rows_list, indent=4, ensure_ascii=False)

    if json_type == 'dynamo':
        with open(output_filename, "a", encoding='utf-8') as jsonfile:
            jsonfile.write(json_object)
            jsonfile.write("\n")
            jsonfile.write("\n")

    else:
        with open(output_filename, "w", encoding='utf-8') as jsonfile:
            jsonfile.write(json_object)


def to_json_dynamo(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        datareader = csv.reader(csvfile)
        next(datareader)
        first_row = next(datareader)
        cur_hashed = hash(first_row[15].strip())
        cur_collection = new_collection(first_row, 'dynamo', cur_hashed)

        for row in datareader:

            hashed = hash(row[15].strip())

            if hashed == cur_hashed:
                add_to_collection(row, cur_collection, 'dynamo')

            else:
                json_write(cur_collection, output_file, 'dynamo')
                cur_hashed = hashed
                cur_collection = new_collection(row, 'dynamo', cur_hashed)

        json_write(cur_collection, output_file, 'dynamo')


def to_json_mongo(input_file, output_file):
    collections = []

    with open(input_file, 'r', encoding='utf-8') as csvfile:
        datareader = csv.reader(csvfile)
        next(datareader)
        first_row = next(datareader)
        cur_hashed = hash(first_row[15].strip())
        cur_collection = new_collection(first_row, 'mongo')

        for row in datareader:

            hashed = hash(row[15].strip())

            if hashed == cur_hashed:
                add_to_collection(row, cur_collection, 'mongo')

            else:
                collections.append(cur_collection)
                cur_hashed = hashed
                cur_collection = new_collection(row, 'mongo')
        collections.append(cur_collection)

    json_write(collections, output_file, 'mongo')


def main(argv):
    input_file = argv[1] + '.csv'
    output_file = argv[1] + '.json'

    while True:
        command = input("What would you like to do?: ")
        if command in commands:
            if command == "help":
                help_commands()
            elif command == "dynamo":
                to_json_dynamo(input_file, output_file)
            elif command == "mongo":
                to_json_mongo(input_file, output_file)

        else:
            print(COMMAND_NOT_FOUND_MSG)
            continue


main(sys.argv)
