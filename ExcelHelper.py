import math

import pandas as pd


def validate_excel_file(data_frame_path):
    try:
        DataFrameToAnalyze = pd.read_excel(io=data_frame_path, sheet_name="TEMPLATE")
        states = DataFrameToAnalyze["ESTADOS"][1:]
        any_non_string_state = states[states.apply(type) != str].any()

        if any_non_string_state:
            raise Exception("All States should be string values.")

        zero_entrance_symbols = DataFrameToAnalyze.iloc[1:, 1].str.split(pat=',')

        for index, value in zero_entrance_symbols.items():

            if type(value) is float:
                continue

            for state in value:
                if state.isnumeric():
                    raise Exception(f"All states on input symbol 0 must be a string, state: {state} is not valid.")

                if not states.str.contains(state).any():
                    raise Exception(
                        f"All states on input symbol 0 must exists on state list, state: {state} is not valid.")

        one_entrance_symbols = DataFrameToAnalyze.iloc[1:, 2].str.split(pat=',')

        for index, value in one_entrance_symbols.items():

            if type(value) is float:
                continue

            for state in value:
                if state.isnumeric():
                    raise Exception(f"All states on input symbol 1 must be a string, state: {state} is not valid.")

                if not states.str.contains(state).any():
                    raise Exception(
                        f"All states on input symbol 1 must exists on state list, state: {state} is not valid.")

        result_states = DataFrameToAnalyze["ACEPTA (1) / RECHAZA (0)"][1:]

        any_non_integer_result_symbol = result_states[result_states.apply(type) != float].any()

        if any_non_integer_result_symbol:
            raise Exception("All state results must be a integer value.")

        all_result_symbols_are_valid = result_states.isin([0, 1]).all()

        if not all_result_symbols_are_valid:
            raise Exception("All state results must be a 0 or a 1 value.")

        return True

    except Exception as e:
        print(f"Error while trying to read file. Description: {e}")
        return False


def is_no_deterministic(data_frame_path):
    DataFrameToAnalyze = pd.read_excel(io=data_frame_path, sheet_name="TEMPLATE")[1:]
    DataFrameToAnalyze.columns = ['STATES', '0', '1', 'RESULT']
    inputs_splitted = DataFrameToAnalyze.iloc[:, 1:3]

    for index, row in inputs_splitted.iterrows():
        zero_input_states_length = [] if type(row['0']) is float else len(row['0'].split(','))
        one_input_states_length = [] if type(row['1']) is float else len(row['1'].split(','))
        if (zero_input_states_length == 0 or zero_input_states_length > 1) or (
                one_input_states_length == 0 or one_input_states_length > 1):
            return True

    return False


def generate_template():
    DataFrameTemplate = pd.DataFrame([['ESTADOS', 'SÍMBOLOS DE ENTRADA', '', 'ACEPTA (1) / RECHAZA (0)'],
                                      ['', 0, 1, '']
                                      ])
    DataFrameTemplate.to_excel(excel_writer="TEMPLATE.xlsx",
                               index=False,
                               header=False,
                               sheet_name='TEMPLATE')
