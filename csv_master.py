import sys
import csv

ERROR_MSG = "ERROR"
COMMAND_NOT_FOUND_MSG = "Command not found. Please enter 'help' for list of commands"

commands = {
    "help",
    "strip: removes whitespace from csv rows",
    "join rows: joins all cells in row and strips whitespace. Optionally alphabetizes",
    "change encoding: changes csv encoding to specified type"
}


def help_commands():
    print(commands)


def get_filename(file_order):
    prompt = "What is the name of your {} file? ".format(file_order)
    filename = ''
    while len(filename) < 2:
        filename = input(prompt)
    return filename


def write_csv(rows_list, output_filename, desired_encoding='utf8'):
    output_file = open(output_filename, 'w', newline='', encoding=desired_encoding)
    writer = csv.writer(output_file)
    writer.writerows(rows_list)
    output_file.close()


def append_csv_rows(rows_list, output_filename, desired_encoding='utf8'):
    output_file = open(output_filename, 'a', newline='', encoding=desired_encoding)
    writer = csv.writer(output_file)
    writer.writerows(rows_list)
    output_file.close()


def strip_whitespace(input_filename, output_filename):
    new_rows_list = []
    with open(input_filename, 'r', encoding="utf8") as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            try:
                original = row[0]
                original = original.strip()
            except:
                original = ERROR_MSG

            new_row = [original]
            new_rows_list.append(new_row)

    write_csv(new_rows_list, output_filename)


def join_cells_into_list(input_filename, output_filename, alphabetize):
    new_rows_list = []
    with open(input_filename, 'r', encoding='unicode_escape') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            new_row = ', '.join(row)
            new_row = new_row.strip()
            tokenized_row = new_row.split(", ")
            if alphabetize:
                tokenized_row.sort()
            tokenized_row = ', '.join(tokenized_row)
            new_rows_list.append([tokenized_row])

        write_csv(new_rows_list, output_filename)


def change_encoding(input_filename, output_filename, current_encoding, desired_encoding):
    new_rows_list = []
    with open(input_filename, 'r', encoding=current_encoding) as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            id = row[0]
            plot = row[1]

            new_row = [id, plot]
            new_rows_list.append(new_row)

        write_csv(new_rows_list, output_filename, desired_encoding)


def main(argv):
    input_file = argv[1]
    output_file = argv[2]

    while True:
        command = input("What would you like to do?: ")
        if command in commands:
            if command == "strip":
                strip_whitespace(input_file, output_file)
            elif command == "help":
                help_commands()
            elif command == "join rows":
                command = input("Would you like to alphabetize? (type 'y' or 'yes' if so): ").lower()
                if command == 'yes' or command == 'y':
                    print("Will alphabetize")
                    join_cells_into_list(input_file, output_file, True)
                else:
                    print("Will not alphabetize")
                    join_cells_into_list(input_file, output_file, False)
            elif command == "change encoding":
                current_encoding = input("What is the input file encoding format?: ").lower()
                desired_encoding = input("What is the desired output file encoding format? (type 'def' or 'default' for utf-8): ").lower()
                if desired_encoding == 'def' or desired_encoding == 'default':
                    print("Changing encoding from", current_encoding, "to utf-8")
                    change_encoding(input_file, output_file, current_encoding)
                else:
                    print("Changing encoding from", current_encoding, "to", desired_encoding)
                    change_encoding(input_file, output_file, current_encoding, desired_encoding)

        else:
            print(COMMAND_NOT_FOUND_MSG)
            continue


main(sys.argv)
