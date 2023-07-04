import csv
import json
import sys

def get_category_dict(row):
    return {
        'high': {
            "S": row[0].strip()
        },
        'mid': {
            "S": row[1].strip()
        },
        'low': {
            "S": row[2].strip()
        },
        'collection': {
            "S": row[3].strip()
        }
    }


def get_types_dict(row):
    return {
        'id_type': {
            "S": row[11].strip()
        },
        'item_type': {
            "S": row[12].strip()
        },
        'association_type': {
            "S": row[13].strip()
        },
        'description_type': {
            "S": row[14].strip()
        }
    }


def get_collection_dict(hashed, category_dict, year, types_dict):
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
            'objects': {
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


def new_collection(row, hashed):
    category_dict = get_category_dict(row)

    divider = row[4].strip()
    entry_id = row[5].strip()
    year = row[6].strip()
    status = row[7].strip()

    entry_dict = get_entry_dict(row, divider)
    types_dict = get_types_dict(row)

    collection_entry = get_collection_dict(hashed, category_dict, year, types_dict)

    if status == '1':
        edit_dict = collection_entry['Item']['objects']['M']['winner']['M']

    else:
        edit_dict = collection_entry['Item']['objects']['M']['nominee']['M']


    edit_dict[entry_id] = entry_dict

    return collection_entry


def add_to_collection(row, cur_collection):
    collection_dict = cur_collection['Item']['objects']['M']
    divider = row[4].strip()
    entry_id = row[5].strip()
    status = row[7].strip()

    if status == '1':
        edit_dict = collection_dict['winner']['M']
    else:
        edit_dict = collection_dict['nominee']['M']

    entry_dict = get_entry_dict(row, divider)

    edit_dict[entry_id] = entry_dict


def get_entry_dict(row, divider):
    entry_dict = {
        "M": {
            'divider': {
                "S": divider
            },
            'item': {
                "S": row[8].strip()
            },
            'association': {
                "S": row[9].strip()
            },
            'description': {
                "S": row[10].strip()
            }
        }
    }

    return entry_dict


def json_write(all_entries, output_file):
    json_object = json.dumps(all_entries, indent=4, ensure_ascii=False)

    with open(output_file, "a", encoding='utf-8') as outfile:
        outfile.write(json_object)
        outfile.write("\n")
        outfile.write("\n")


def main(argv):
    filename = argv[1]
    input_file = filename + '.csv'
    output_file = filename + '.json'

    with open(input_file, 'r', encoding='utf-8') as csvfile:
        datareader = csv.reader(csvfile)

        next(datareader)
        first_row = next(datareader)

        cur_hashed = hash(first_row[15].strip())
        cur_collection = new_collection(first_row, cur_hashed)

        for row in datareader:

            hashed = hash(row[15].strip())

            if hashed == cur_hashed:
                add_to_collection(row, cur_collection)

            else:
                json_write(cur_collection, output_file)
                cur_hashed = hashed
                cur_collection = new_collection(row, cur_hashed)

        json_write(cur_collection, output_file)


main(sys.argv)

