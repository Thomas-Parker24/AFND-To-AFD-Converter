import sys

from ExcelHelper import generate_template, validate_excel_file, is_no_deterministic

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print("Validating excel...")
    if not validate_excel_file("TEMPLATE.xlsx"):
        print("Excel file is not valid.")
        sys.exit()

    print("Excel file is valid!")
    print("Validating automata...")
    if not is_no_deterministic("TEMPLATE.xlsx"):
        print("Automata is deterministic.")
        sys.exit()

    print("Automata is no deterministic!")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
