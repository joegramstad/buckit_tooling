import sys
import csv

ERROR_MSG = "ERROR"
COMMAND_NOT_FOUND_MSG = "Command not found. Please enter 'help' for list of commands"

commands = {
    "strip",
    "help",
}

def help_commands():
    print(commands)


def get_filename(file_order):
    prompt = "What is the name of your {} file? ".format(file_order)
    filename = ''
    while len(filename) < 2:
        filename = input(prompt)
    return filename


def write_csv(rows_list, output_filename):
    output_file = open(output_filename, 'w', newline='', encoding="utf8")
    writer = csv.writer(output_file)
    writer.writerows(rows_list)
    output_file.close()


def append_csv_rows(rows_list, output_filename):
    output_file = open(output_filename, 'a', newline='', encoding="utf8")
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
            print(new_row)
            new_rows_list.append(new_row)

    write_csv(new_rows_list, output_filename)


def main(argv):

    while True:
        command = input("What would you like to do? ")
        if command in commands:


        else:
            print(COMMAND_NOT_FOUND_MSG)
            continue



main(sys.argv)
