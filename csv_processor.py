import csv
import sys
import re

WS_ERROR_MSG = "(ERROR) "


# def replace_char_map(input_filename, intermediate_filename):
#     res = set(test_dict.values())
#     with open(input_filename, 'r', encoding='utf-8-sig') as input_file:
#         data_reader = csv.reader(input_file)
#
#         for line in ansi_file:
#             print("original_line: " + line)
#             utf_file.write(line)

def write_csv(rows_list, output_filename, desired_encoding='utf-8'):
    output_file = open(output_filename, 'w', newline='', encoding=desired_encoding)
    writer = csv.writer(output_file)
    writer.writerows(rows_list)
    output_file.close()


def load_char_mappings():
    with open('char_map.csv', 'r', encoding="utf-8-sig") as f:
        reader = csv.reader(f, skipinitialspace=True)
        result = dict(reader)
        return result


def strip_whitespace(i, cell):
    try:
        print("cell ", i, cell)
        new_cell = cell.strip()
    except:
        print("cell ", i, WS_ERROR_MSG)
        new_cell = WS_ERROR_MSG + ' ' + cell

    return new_cell


def main(argv):
    input_filename = argv[1]
    output_filename = argv[2]

    CHAR_MAP = load_char_mappings()

    new_rows_list = []

    with open(input_filename, 'r', encoding="utf-8-sig") as input_file:
        data_reader = csv.reader(input_file)
        for row in data_reader:
            new_row = []
            unknown_encodings = []
            print("row ", row)
            for i, cell in enumerate(row):
                ## START CELL TRANSFORMS HERE
                stripped_cell = strip_whitespace(i, cell)
                if regex_result := re.findall("\D*\?\D+", stripped_cell):
                    unknown_encodings.extend(regex_result)

                ## END CELL TRANSFORMS HERE

                new_row.append(stripped_cell)

            new_row.extend(unknown_encodings)

            new_rows_list.append(new_row)

    write_csv(new_rows_list, output_filename)


main(sys.argv)
