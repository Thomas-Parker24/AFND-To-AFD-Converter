import pandas as pd


def validate_excel_file(data_frame_path):
    try:
        DataFrameToAnalyze = pd.read_excel(io=data_frame_path, sheet_name="TEMPLATE")
        states = DataFrameToAnalyze["ESTADOS"][1:]
        any_non_string_state = states[states.apply(type) != str].any()

        if any_non_string_state:
            raise Exception("All States should be string values.")

        zero_entrance_symbols = DataFrameToAnalyze.iloc[1:,1]
        any_non_string_zero_input_symbol = zero_entrance_symbols[zero_entrance_symbols.apply(type) != str].any()

        if any_non_string_zero_input_symbol:
            raise Exception("All states on input symbol 0 must be a string.")

        all_zero_entrance_sates_are_valid = zero_entrance_symbols.isin(states).all()

        if not all_zero_entrance_sates_are_valid:
            raise Exception("All states on input symbol 0 must exists on state list.")

        one_entrance_symbols = DataFrameToAnalyze.iloc[1:,2]
        any_non_string_one_input_symbol = one_entrance_symbols[one_entrance_symbols.apply(type) != str].any()

        if any_non_string_one_input_symbol:
            raise Exception("All states on input symbol 1 must be a string.")

        all_one_input_states_are_valid = one_entrance_symbols.isin(states).all()

        if not all_one_input_states_are_valid:
            raise Exception("All states on input symbol 1 must exists on state list.")

        result_states = DataFrameToAnalyze["ACEPTA (1) / RECHAZA (0)"][1:]

        any_non_integer_result_symbol = result_states[result_states.apply(type) != float].any()

        if any_non_integer_result_symbol:
            raise Exception("All state results must be a integer value.")

        all_result_symbols_are_valid = result_states.isin([0,1]).all()

        if not all_result_symbols_are_valid:
            raise Exception("All state results must be a 0 or a 1 value.")

        print("Excel file passed all validations!")

    except Exception as e:
        print(f"Error while trying to read file. Description: {e}")


def generate_template():
    DataFrameTemplate = pd.DataFrame([['ESTADOS', 'SÍMBOLOS DE ENTRADA', '', 'ACEPTA (1) / RECHAZA (0)'],
                                      ['', 0, 1, '']
                                      ])
    DataFrameTemplate.to_excel(excel_writer="TEMPLATE.xlsx",
                               index=False,
                               header=False,
                               sheet_name='TEMPLATE')
