import sys
import pandas as pd
from ExcelHelper import generate_template, validate_excel_file, is_no_deterministic, convert_to_deterministict
from PrintingHelper import generate_deterministict_automata_graphic,generate_no_deterministict_automata_graphic
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

    print("Generating no deterministic plot...")
    DataFrameToAnalyze = pd.read_excel(io="TEMPLATE.xlsx", sheet_name="TEMPLATE")[1:]
    DataFrameToAnalyze.columns = ['STATES', '0', '1', 'RESULT']
    generate_no_deterministict_automata_graphic("Automata no determinístico", DataFrameToAnalyze)


    print("Automata is no deterministic!")
    print("Converting into deterministic.")
    data = convert_to_deterministict("TEMPLATE.xlsx")

    print("Generating deterministic plot...")
    generate_deterministict_automata_graphic("Automata determinístico", data)