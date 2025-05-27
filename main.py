import sys
import os
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

    DataFrameToAnalyze = pd.read_excel(io="TEMPLATE.xlsx", sheet_name="TEMPLATE")[1:]
    DataFrameToAnalyze.columns = ['STATES', '0', '1', 'RESULT']

    if not is_no_deterministic("TEMPLATE.xlsx"):
        print("Automata is deterministic.")
        generate_deterministict_automata_graphic("Automata determinístico", DataFrameToAnalyze)
        os.startfile(os.getcwd() + r"\renders\Automata determinístico.pdf")
        sys.exit()

    print("\n##### NO DETERMINISTICT AUTOMATA ######\n")
    print(DataFrameToAnalyze)
    print("\n#######################################\n")


    print("Generating no deterministic plot...")
    generate_no_deterministict_automata_graphic("Automata no determinístico", DataFrameToAnalyze)


    print("Automata is no deterministic!")
    print("Converting into deterministic.")
    data = convert_to_deterministict("TEMPLATE.xlsx")

    print("\n####### DETERMINISTICT AUTOMATA #######\n")
    print(data)
    print("\n#######################################\n")

    print("Generating deterministic plot...")
    generate_deterministict_automata_graphic("Automata determinístico", data)

    os.startfile(os.getcwd() + r"\renders\Automata determinístico.pdf")
    os.startfile(os.getcwd() + r"\renders\Automata no determinístico.pdf")